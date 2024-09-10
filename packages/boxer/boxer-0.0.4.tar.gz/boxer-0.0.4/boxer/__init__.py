# SPDX-FileCopyrightText: 2024 OpenBit
#
# SPDX-License-Identifier: MIT

"""
Boxer - A VM Builder

Boxer allows you to create system images from code.
Built on Python, it leverages asyncio to so you can run multiple images in parallel.
You don't need to learn new languages to build your images, everything is done using Python.
"""
from boxer._internal.cli import Command  # noqa: F401
from boxer._internal.builder import Builder  # noqa: F401
from boxer._internal.transport import Transport  # noqa: F401
from boxer._internal.version import VERSION

__version__ = VERSION
