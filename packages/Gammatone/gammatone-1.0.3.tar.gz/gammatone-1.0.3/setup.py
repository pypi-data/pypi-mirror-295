# Copyright 2014 Jason Heeris, jason.heeris@gmail.com
#
# This file is part of the gammatone toolkit, and is licensed under the 3-clause
# BSD license: https://github.com/detly/gammatone/blob/master/COPYING
import os

from setuptools import find_packages, setup

_PATH_ROOT = os.path.dirname(__file__)

with open(os.path.join(_PATH_ROOT, "README.md"), encoding="utf-8") as fo:
    README = fo.read()
# replace relative links with absolute links
README = README.replace("](docs/", "](https://github.com/Lightning-Sandbox/gammatone/raw/main/docs/")

setup(
    name="Gammatone",
    version="1.0.3",
    author="Jason Heeris",
    author_email="Jason@Heeri.me",
    url="https://github.com/Lightning-Sandbox/gammatone",
    download_url="https://github.com/Lightning-Sandbox/gammatone/archive/main.zip",
    long_description=README,
    python_requires=">=3.8",
    long_description_content_type="text/markdown",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=["numpy", "scipy", "matplotlib"],
    extras_require={"test": ["pytest", "mock"]},
    entry_points={"console_scripts": ["gammatone = gammatone.plot:main"]},
    classifiers=[
        "Environment :: Console",
        "Natural Language :: English",
        # How mature is this project? Common values are
        #   3 - Alpha, 4 - Beta, 5 - Production/Stable
        "Development Status :: 4 - Beta",
        # Indicate who your project is intended for
        "Intended Audience :: Developers",
        "Topic :: Scientific/Engineering :: Information Analysis",
        # Pick your license as you wish
        "Operating System :: OS Independent",
        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both.
        "Programming Language :: Python :: 3",
    ],
)
