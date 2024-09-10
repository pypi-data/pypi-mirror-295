# SPDX-FileCopyrightText: 2024 OpenBit
#
# SPDX-License-Identifier: MIT

"""Boxer exceptions

Custom exceptions used within Boxer
"""


class BoxerException(Exception):
    """Base exception for Boxer"""


class MissingRequirement(BoxerException):
    """Exception used when a required Python requirement isn't installed"""


class ProcessError(BoxerException):
    """When a subprocess (local or remote) fails"""


class RequiredBinaryError(BoxerException):
    """A builder requires a local binary that is not available"""


class HTTPException(BoxerException):
    """When a HTTP client error happens"""


class MissingHTTPSession(BoxerException):
    """When a HTTP session isn't set"""
