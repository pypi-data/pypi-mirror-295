#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""HARPIA-MM Python library dependency checker.

Programmatically check whether the dependencies required to run harpiamm
scripts are satisfied. This is particularly useful when running scripts from
the LC Launcher App and for the FLIR spinnaker-python/PySpin library which is
not available from PyPi.

This script is a part of the HARPIA Microscopy Kit, which is a set of tools for
the alignment, characterization and troubleshooting of HARPIA-MM Microscopy
Extension.

Contact: lukas.kontenis@lightcon.com, support@lightcon.com

Copyright (c) 2019-2024 Light Conversion
All rights reserved.
www.lightcon.com
"""
from packaging import version
import harpiamm

import subprocess
import sys

def install(package_name):
    subprocess.check_call([sys.executable, "-m", "pip", "install", "--upgrade", package_name])

def check_ver(package, min_ver):
    if version.parse(package.__version__) < version.parse(min_ver):
        print(f"This script requires {package.__name__} {min_ver} or newer")
        print(f"Installing...")
        install(package.__name__)

        if version.parse(package.__version__) < version.parse(min_ver):
            raise RuntimeError(f"This example requires {package.__name__} {min_ver}, but it was not found and could not be installed automatically")

def harpiamm_dep_check():
    check_ver(harpiamm, "2.0.0")
