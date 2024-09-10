# SPDX-FileCopyrightText: 2024 OpenBit
# SPDX-FileContributor: Hugo Rodrigues
#
# SPDX-License-Identifier: MIT
"""Variables related to our version

The versions is fetched from the package metadata
since it's set during build. If we are unable to
get the installed package version, we assume next
"""

import importlib.metadata

try:
    VERSION = importlib.metadata.version("boxer")
except importlib.metadata.PackageNotFoundError:
    VERSION = "next"
