#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# flake8: noqa
from __future__ import absolute_import
from __future__ import print_function

import io
import sys
from os import path

from setuptools import setup

here = path.abspath(path.dirname(__file__))


def read(*names, **kwargs):
    return io.open(path.join(here, *names), encoding=kwargs.get("encoding", "utf8")).read()


REQUIRED_MAJOR = 3
REQUIRED_MINOR = 9

# Check if the installed Python version matches the required one
if sys.version_info < (REQUIRED_MAJOR, REQUIRED_MINOR):
    error = "Installation requires python >= {required_major}.{required_minor}, but you're trying to install it on python {major}.{minor}.".format(
        major=sys.version_info.major,
        minor=sys.version_info.minor,
        required_minor=REQUIRED_MINOR,
        required_major=REQUIRED_MAJOR,
    )
    sys.exit(error)


long_description = read("README.md")
requirements = read("requirements.txt").split("\n")

# Pin the numpy version < 2 on Windows, due to incompatibility issues with torch
# See: https://github.com/pytorch/pytorch/issues/131668
if sys.platform == "win32":
    index = [i for i, req in enumerate(requirements) if "numpy" in req][0]
    requirements[index] = "numpy<2"

about = {}
exec(read("src", "aixd", "__version__.py"), about)

setup(
    name=about["__title__"],
    version=about["__version__"],
    license=about["__license__"],
    author=about["__author__"],
    author_email=about["__author_email__"],
    url=about["__url__"],
    description=about["__description__"],
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=["aixd"],
    package_dir={"": "src"},
    include_package_data=True,
    zip_safe=False,
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Operating System :: Unix",
        "Operating System :: POSIX",
        "Operating System :: Microsoft :: Windows",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: Implementation :: CPython",
        "Topic :: Scientific/Engineering",
    ],
    keywords=[],
    install_requires=requirements,
    extras_require={
        "dev": [
            "black",
            "bump2version >=1.0.1",
            "compas_invocations >=1.0.0",
            "flake8",
            "invoke >=0.14",
            "isort",
            "nbsphinx",
            "pytest >=6.0",
            "sphinx",
            "pydata-sphinx-theme",
            "check-manifest >=0.36",
            "scp",
            "paramiko",
        ],
        "examples": ["jupyter", "ipython >=5.8", "ipykernel", "pythreejs", "matplotlib", "rich >= 10.2.2"],
    },
    entry_points={},
)
