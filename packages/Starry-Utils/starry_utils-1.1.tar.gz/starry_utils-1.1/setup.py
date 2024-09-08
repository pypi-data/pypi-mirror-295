import setuptools  # isort:skip

import os
import re

with open("README.md", mode="r") as f:
    long_description = f.read()

with open(
    os.path.join(os.path.join(os.path.dirname(__file__), "Star_Utils"), "__version__.py"),
    mode="r",
) as file:
    content = file.read()
__version__ = float(
    re.compile(r"__version__\s*=\s*(?P<version>\d+\.\d+)").search(content).groupdict()["version"]
)

setuptools.setup(
    name="Starry-Utils",
    version=str(__version__),
    author="Star",
    author_email="skylar.rae.val@proton.me",
    description="Utils for Star-Cogs.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/LeDeathAmongst/Star_Utils",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.9.1",
    install_requires=[
        "sentry_sdk",
        "colorama",
    ],
)
