from redbot.core import commands  # isort:skip
from redbot.core.bot import Red  # isort:skip
from redbot.core import Config  # isort:skip
import typing  # isort:skip
import discord  # isort:skip

import asyncio
import re
from uuid import uuid4

import sentry_sdk
from redbot.core import __version__ as red_version
from redbot.core.utils.common_filters import INVITE_URL_RE

from .cogsutils import CogsUtils
from .loop import Loop

SNOWFLAKE_REGEX = r"\b\d{17,20}\b"
IP_V4_REGEX = (
    r"(\b25[0-5]|\b2[0-4][0-9]|\b[01]?[0-9][0-9]?)(\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)){3}"
)
IP_V6_REGEX = r"(([0-9a-fA-F]{1,4}:){7,7}[0-9a-fA-F]{1,4}|([0-9a-fA-F]{1,4}:){1,7}:|([0-9a-fA-F]{1,4}:){1,6}:[0-9a-fA-F]{1,4}|([0-9a-fA-F]{1,4}:){1,5}(:[0-9a-fA-F]{1,4}){1,2}|([0-9a-fA-F]{1,4}:){1,4}(:[0-9a-fA-F]{1,4}){1,3}|([0-9a-fA-F]{1,4}:){1,3}(:[0-9a-fA-F]{1,4}){1,4}|([0-9a-fA-F]{1,4}:){1,2}(:[0-9a-fA-F]{1,4}){1,5}|[0-9a-fA-F]{1,4}:((:[0-9a-fA-F]{1,4}){1,6})|:((:[0-9a-fA-F]{1,4}){1,7}|:)|fe80:(:[0-9a-fA-F]{0,4}){0,4}%[0-9a-zA-Z]{1,}|::(ffff(:0{1,4}){0,1}:){0,1}((25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])\.){3,3}(25[0-5]|(2[0-4]|1{0-1}[0-9]){0,1}[0-9])|([0-9a-fA-F]{1,4}:){1,4}:((25[0-5]|(2[0-4]|1{0-1}[0-9]){0,1}[0-9])\.){3,3}(25[0-5]|(2[0-4]|1{0-1}[0-9]){0,1}[0-9]))"

SENTRY_DSN = (
    "https://463fef380c8d6f900e3deec882110429@o4507885141753856.ingest.us.sentry.io/4507887488598016"
)

def _(untranslated: str) -> str:
    return untranslated

SENTRY_MASTER_MSG = _(
    "Hey there! This looks like the first time you're using Star's cogs (or you just updated to a"
    " version which supports this). To help make this cog, and all my others, as good and bug-free"
    " as possible, I have **opt-in** telemetry and error reporting __which affects all of my"
    " (github.com/LeDeathAmongst's) cogs__ on the Star-Cogs repository, using Sentry. The telemetry"
    " consists of data on the cog release and performance data of background tasks and loops (if"
    " applicable), and error reporting means that if something goes wrong the error and some"
    " associated data will be automatically sent to me so I can fix it quickly.\n\nA best effort"
    " is made to ensure no sensitive data is transmitted. For more information, including some"
    " technical details, visit"
    " <https://Star-cogs.readthedocs.io/en/latest/repo_telemetry.html>\n\n**If you would like to"
    " opt-in to telemetry and error reporting, and help me develop my cogs, run the command"
    " `[p]star_utils telemetrywithsentry True`. `[p]` is your prefix.**\nNo data is collected"
    " relating to command usage."
)
SENTRY_REMINDER_ON = _(
    "Hey there! You just installed Star's {} cog. This is a reminder that you previously enabled"
    " telemetry and error reporting, which applies to all of my cogs, and this one is no"
    " different.\n\nI would like to emphasize again that a best effort it made to remove sensitive"
    " data. You can see <https://Star-cogs.readthedocs.io/en/latest/repo_telemetry.html> for more"
    " details and change your choice at any time with the `[p]Star_utils telemetrywithsentry"
    " False` command, applying to all my cogs."
)
SENTRY_REMINDER_OFF = _(
    "Hey there! You just installed Star's {} cog. This is a reminder that you previously chose"
    " not to enable telemetry and error reporting, which is also available in this cog. I hope you"
    " don't mind this reminder.\n\nI would like to emphasize again that a best effort it made to"
    " remove sensitive data. You can see"
    " <https://Star-cogs.readthedocs.io/en/latest/repo_telemetry.html> for more details and"
    " change your choice at any time with the `[p]Star_utils telemetrywithsentry True` command,"
    " applying to all my cogs."
)

__all__ = ["SentryHelper"]

class SentryHelper:
    def __init__(self, bot: Red, cog: commands.Cog) -> None:
        if cog.qualified_name != "Star_Utils":
            raise ValueError(cog.qualified_name)
        self.bot: Red = bot
        self.cog: commands.Cog = cog

        self.last_errors: typing.Dict[
            str, typing.Dict[str, typing.Union[commands.Context, Exception]]
        ] = {}

        self.sentry_enabled: bool = None
        self.display_sentry_manual_command: bool = None
        self.send_reminders: bool = True
        self.uuid: typing.Optional[str] = None
        self.hubs: typing.Dict[str, sentry_sdk.Hub] = {}

        self.config: Config = cog.config
        self.sentry_global: typing.Dict[
            str, typing.Dict[str, typing.Union[int, bool, typing.Optional[str], typing.List[str]]]
        ] = {
            "sentry": {
                "version": 1,
                "sentry_enabled": False,
                "display_sentry_manual_command": True,
                "master_msg_sent": False,
                "uuid": None,
                "cogs_notified": [],
            }
        }
        self.config.register_global(**self.sentry_global)

        asyncio.create_task(self._async_init())
        self.cog.loops.append(
            Loop(
                cog=self.cog,
                name="Sentry Helper",
                function=self.periodic_session_restart,
                hours=1,
            )
        )

        self.dont_send_reminders: bool = False
        self.ready: asyncio.Event = asyncio.Event()

    async def _async_init(self) -> None:
        self.sentry_enabled = await self.config.sentry.sentry_enabled()
        self.display_sentry_manual_command = not self.sentry_enabled and (
            await self.config.sentry.display_sentry_manual_command()
        )
        uuid = await self.config.sentry.uuid()
        if uuid is None:
            uuid = str(uuid4())
            await self.config.sentry.uuid.set(uuid)
        self.uuid = uuid
        self.ready.set()

    async def periodic_session_restart(self) -> None:
        if not self.sentry_enabled:
            return
        for hub in self.hubs.values():
            hub.end_session()
            hub.start_session()

    async def send_command_error(
        self,
        ctx: commands.Context,
        error: commands.CommandError,
        manually: typing.Optional[bool] = False,
    ) -> typing.Optional[typing.Union[str, bool]]:
        try:
            if ctx.cog is None:
                return
            if not manually and not self.sentry_enabled:
                return False
            hub = await self.get_sentry_hub(ctx.cog)
            if hub is None:
                return
            if isinstance(error, commands.CommandInvokeError):
                if isinstance(ctx.command, discord.ext.commands.HybridCommand):
                    _type = "[hybrid|text]"
                else:
                    _type = "[text]"
            elif isinstance(error, commands.HybridCommandError):
                _type = "[hybrid|slash]"
            else:
                return False
            message = f"Error in {_type} command '{ctx.command.qualified_name}'."
            with sentry_sdk.isolation_scope() as scope:
                hub.add_breadcrumb(category="command", message=message)
                scope.set_extra("user_permissions", ctx.permissions)
                scope.set_extra("user_permissions_dict", dict(ctx.permissions))
                scope.set_extra("bot_permissions", ctx.bot_permissions)
                scope.set_extra("bot_permissions_dict", dict(ctx.bot_permissions))
                try:
                    e = error.original  # type:ignore
                except AttributeError:
                    e = error
                event_id = hub.capture_exception(e)
                scope._extras.clear()
            return event_id
        except Exception as e:
            if manually:
                raise e
            self.cog.logger.error("Sending an error to Sentry failed.", exc_info=e)
            return False

    def remove_sensitive_data(self, event: dict, hint: typing.Optional[dict] = {}) -> typing.Dict:
        """Remove sensitive data from the event. This should only be used by the Sentry SDK.
        This has two main parts:
        1) Remove any mentions of the bot's token
        2) Replace all IDs with a 4 digit number which originates from the timestamp of the ID
        3) Remove discord invites
        4) Replace var paths (userprofile, home, computer name, user name)
        Parameters
        ----------
        event : dict
            Event data
        hint : dict
            Event hint
        Returns
        -------
        dict
            The event dict with above stated sensitive data removed.
        """

        def regex_stuff(s: str) -> str:
            """Shorten any Discord IDs/snowflakes (basically any number 17-20 characters) to 4 digits
            by locating the timestamp and getting the last 4 digits - the milliseconds and the last
            digit of the second countsecond.
            Parameters
            ----------
            s : str
                String to shorten IDs in
            Returns
            -------
            str
                String with IDs shortened
            """
            s = re.sub(
                SNOWFLAKE_REGEX,
                lambda m: f"[SHORTENED-ID-{str(int(m.group()) >> 22)[-4:]}]",
                s,
            )
            s = re.sub(IP_V4_REGEX, "IP_V4", s)
            s = re.sub(IP_V6_REGEX, "IP_V6", s)
            return re.sub(INVITE_URL_RE, "[DISCORD-INVITE-LINK]", s)

        def recursive_replace(
            d: typing.Union[typing.Dict[str, typing.Any], typing.List, str], token: str
        ) -> typing.Union[dict, str]:
            """Recursively replace text in keys and values of a dictionary.
            Parameters
            ----------
            d : Union[Dict[str, Any], str]
                Dict or item to replace text in
            token : str
                Token to remove
            Returns
            -------
            dict
                Safe dict
            """
            if isinstance(d, typing.Dict):
                return {
                    CogsUtils.replace_var_paths(regex_stuff(k.replace(token, "[BOT-TOKEN]")))
                    if isinstance(k, str)
                    else k: recursive_replace(v, token)
                    for k, v in d.items()
                }
            elif isinstance(d, typing.List):
                return [
                    CogsUtils.replace_var_paths(regex_stuff(recursive_replace(i, token)))
                    if isinstance(i, str)
                    else recursive_replace(i, token)
                    for i in d
                ]
            return (
                CogsUtils.replace_var_paths(regex_stuff(d.replace(token, "[BOT_TOKEN]")))
                if isinstance(d, str)
                else d
            )

        token = self.bot.http.token

        return recursive_replace(event, token)  # type:ignore

    async def enable_sentry(self) -> None:
        """Enable Sentry telemetry and error reporting."""
        await self.config.sentry.sentry_enabled.set(True)
        self.sentry_enabled = True
        self.dont_send_reminders = False
        for hub in self.hubs.values():
            hub.start_session()

    async def disable_sentry(self) -> None:
        """Disable Sentry telemetry and error reporting."""
        await self.config.sentry.sentry_enabled.set(False)
        self.sentry_enabled = False
        self.dont_send_reminders = True

        for hub in self.hubs.values():
            hub.end_session()

    async def get_sentry_hub(
        self, cog: commands.Cog, force: typing.Optional[bool] = False
    ) -> sentry_sdk.Hub:
        """Get a Sentry Hub and Client for a DSN. Each cog should have its own hub.
        Returns
        -------
        Hub
            A Sentry Hub with a Client
        """
        if not self.ready.is_set():
            await self.ready.wait()
        if cog.qualified_name in self.hubs and not force:
            return self.hubs[cog.qualified_name]
        if getattr(cog, "__version__", None) is None and getattr(cog, "__commit__", None) is None:
            try:
                nb_commits, version, commit = await CogsUtils.get_cog_version(
                    bot=self.bot, cog=self.cog
                )
                cog.__version__ = version
                cog.__commit__ = commit
            except Exception:
                pass
        client = sentry_sdk.Client(
            dsn=SENTRY_DSN,
            traces_sample_rate=0.005,
            before_send=self.remove_sensitive_data,
            before_breadcrumb=self.remove_sensitive_data,
            release=(
                f"Star-Cogs|{cog.qualified_name}@{getattr(cog, '__version__', 1.0)}|{getattr(cog, '__commit__', '')}"
            ),
            debug=False,
            max_breadcrumbs=25,
            server_name="[EXPUNGED]",
        )

        scope = sentry_sdk.Scope()
        scope.set_tag("cog_name", cog.qualified_name)
        scope.set_tag("cog_version", getattr(cog, "__version__", 1.0))
        scope.set_tag("cog_commit", getattr(cog, "__commit__", ""))
        scope.set_tag("red_release", red_version)
        scope.set_tag("dpy_release", discord.__version__)
        scope.set_user({"id": self.uuid})

        hub = sentry_sdk.Hub(client, scope)
        self.hubs[cog.qualified_name] = hub

        hub.start_session()
        return hub

    async def cog_unload(self, cog: commands.Cog) -> sentry_sdk.Hub:
        """Close the linked Sentry Hub.
        Returns
        -------
        Hub
            A Sentry Hub closed
        """
        hub = self.hubs.get(cog.qualified_name, None)
        if hub is None:
            return None
        hub.end_session()
        hub.client.close()
        del self.hubs[cog.qualified_name]
        return hub

    async def maybe_send_owners(self, cog: commands.Cog) -> None:
        if not self.ready.is_set():
            await self.ready.wait()
        if (
            self.cog is None
            or not hasattr(self.cog, "telemetrywithsentry")
            or getattr(self.cog.telemetrywithsentry, "__is_dev__", False)
        ):
            return  # Not send automatically errors to Sentry for the moment.
        if not await self.config.sentry.master_msg_sent():
            self.dont_send_reminders = True
            await self.config.sentry.master_msg_sent.set(True)
            try:
                await self.bot.send_to_owners(SENTRY_MASTER_MSG.format(cog.qualified_name))
            except Exception:
                pass
            async with self.config.sentry.cogs_notified() as c_n:
                c_n.append(cog.qualified_name)
            return

        if cog.qualified_name in await self.config.sentry.cogs_notified():
            return
        if self.dont_send_reminders:
            async with self.config.sentry.cogs_notified() as c_n:
                c_n.append(cog.qualified_name)
            return
        try:
            if self.sentry_enabled:
                await self.bot.send_to_owners(SENTRY_REMINDER_ON.format(cog.qualified_name))
            else:
                self.dont_send_reminders = True
                await self.bot.send_to_owners(SENTRY_REMINDER_OFF.format(cog.qualified_name))
        except Exception:
            pass
        async with self.config.sentry.cogs_notified() as c_n:
            c_n.append(cog.qualified_name)
