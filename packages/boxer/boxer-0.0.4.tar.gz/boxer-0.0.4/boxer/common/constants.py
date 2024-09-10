# SPDX-FileCopyrightText: 2024 OpenBit
#
# SPDX-License-Identifier: MIT

"""
Constants used across the project
"""
import os
from pathlib import Path
import re

CACHE_PATH = os.path.join(Path.home(), ".cache", "boxer")
DOWNLOAD_PATH = os.path.join(CACHE_PATH, "download")

RE_MODULE_CLASS = re.compile(r"(.+)\.(.+)")
