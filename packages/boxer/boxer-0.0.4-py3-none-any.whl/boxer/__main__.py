# SPDX-FileCopyrightText: 2024 OpenBit
#
# SPDX-License-Identifier: MIT

"""Boxer - A VM builder"""

# Setup logging with warnings before importing any other package
import logging
import sys
import warnings

LOG_HANDLER = logging.StreamHandler()
if sys.version_info.minor > 11:
    LOG_FORMAT = "%(asctime)s %(levelname)s %(taskName)s: %(message)s"
else:
    LOG_FORMAT = "%(asctime)s %(levelname)s: %(message)s"  # Python 3.11 doesn't have taskName
LOG_HANDLER.setFormatter(logging.Formatter(LOG_FORMAT))

LOGGER = logging.getLogger()
LOGGER.addHandler(LOG_HANDLER)
if "--verbose" in sys.argv:
    LOGGER.setLevel(logging.DEBUG)
else:
    LOGGER.setLevel(logging.INFO)

warnings.simplefilter('default', category=DeprecationWarning)
warnings.simplefilter('default', category=RuntimeWarning)

from boxer._internal.cli import main  # pylint: disable=wrong-import-position # noqa: E402
# Register builtin commands
import boxer.cli  # pylint: disable=unused-import,wrong-import-position # noqa: F401,E402


def wrapper():
    """Wrap sys.exit for real main

    This is to ensure that running boxer as a module or binary
    has the same behaviour.
    """
    sys.exit(main())


if __name__ == "__main__":
    wrapper()
