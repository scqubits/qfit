"""qfit: data extraction GUI tool for use with scQuibts
==============================================================

qfit is part of scQubits, an an open-source Python package for simulating superconducting qubits. The qfit package
provides a GUI tool for loading and displaying data, for example from spectroscopy experiments. The GUI simplifies the
extraction of data points from measurement results, as required for fitting experimental data to theoretical qubit
models.
"""

#
# This file is part of qfit.
#
#    Copyright (c) 2023, Tianpu Zhao, Danyang Chen, Jens Koch
#    All rights reserved.
#
#    This source code is licensed under the BSD-style license found in the
#    LICENSE file in the root directory of this source tree.
############################################################################

import os
import sys

from setuptools import setup, find_packages

DOCLINES = __doc__.split("\n")

CLASSIFIERS = """\
Development Status :: 4 - Beta
Intended Audience :: Science/Research
License :: OSI Approved :: BSD License
Programming Language :: Python
Programming Language :: Python :: 3
Topic :: Scientific/Engineering
Operating System :: MacOS
Operating System :: POSIX
Operating System :: Unix
Operating System :: Microsoft :: Windows
"""


EXTRA_KWARGS = {}


# all information about scqubits goes here
MAJOR = 2
MINOR = 0
MICRO = 1
ISRELEASED = True


VERSION = "%d.%d.%d" % (MAJOR, MINOR, MICRO)

CURDIR = os.path.dirname(os.path.abspath(__file__))
with open(os.path.join(CURDIR, "requirements.txt")) as requirements:
    INSTALL_REQUIRES = requirements.read().splitlines()


PACKAGES = find_packages()


PYTHON_VERSION = ">=3.10"


NAME = "qfit"
AUTHOR = "Tianpu Zhao, Danyang Chen, Jens Koch"
AUTHOR_EMAIL = (
    "tianpuzhao2022@u.northwestern.edu, "
    "danyangchen2026@u.northwestern.edu, "
    "jens-koch@northwestern.edu"
)
LICENSE = "BSD"

with open(os.path.join(CURDIR, 'README.md'), encoding='utf-8') as f:
    README_CONTENT = f.read().split("\n")

DESCRIPTION = README_CONTENT[0]
LONG_DESCRIPTION = "\n".join(README_CONTENT[2:])
KEYWORDS = "parameter extraction, superconducting qubits"

URL = "https://github.com/scqubits/qfit"

CLASSIFIERS = [_f for _f in CLASSIFIERS.split("\n") if _f]
PLATFORMS = ["Linux", "Mac OSX", "Unix", "Windows"]


def git_short_hash():
    try:
        git_str = "+" + os.popen('git log -1 --format="%h"').read().strip()
    except OSError:
        git_str = ""
    else:
        if git_str == "+":  # fixes setuptools PEP issues with versioning
            git_str = ""
    return git_str


FULLVERSION = VERSION
if not ISRELEASED:
    FULLVERSION += ".dev" + str(MICRO) + git_short_hash()


def write_version_py():
    cnt = """\
# THIS FILE IS GENERATED FROM qfit SETUP.PY
short_version = '%(version)s'
version = '%(fullversion)s'
release = %(isrelease)s
"""
    version_path = os.path.join(CURDIR, 'qfit', 'version.py')

    with open(version_path, "w") as versionfile:
        versionfile.write(
            cnt
            % {
                "version": VERSION,
                "fullversion": FULLVERSION,
                "isrelease": str(ISRELEASED),
            }
        )

write_version_py()


# Setup commands go here
setup(
    name=NAME,
    version=FULLVERSION,
    packages=PACKAGES,
    author=AUTHOR,
    author_email=AUTHOR_EMAIL,
    license=LICENSE,
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    keywords=KEYWORDS,
    # url=URL,
    classifiers=CLASSIFIERS,
    platforms=PLATFORMS,
    zip_safe=False,
    include_package_data=True,
    install_requires=INSTALL_REQUIRES,
    python_requires=PYTHON_VERSION,
    **EXTRA_KWARGS
)
