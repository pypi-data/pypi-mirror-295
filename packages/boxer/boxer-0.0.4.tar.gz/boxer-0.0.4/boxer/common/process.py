# SPDX-FileCopyrightText: 2024 OpenBit
#
# SPDX-License-Identifier: MIT

"""
Common functions for process handling
"""
import asyncio
import logging
import os

from .exceptions import ProcessError

LOGGER = logging.getLogger(__name__)


async def execute(cmd: str, *args: any, stdin: any = None, valid_exit_codes: list = None, raise_on_error: bool = True, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE) -> tuple:
    """Execute a command.

    It returns the exit code, stdout and stderr.
    If raise_on_error is True (default), it raises a Exception if the exit code isn't in valid_exit_codes

    Args:
        command: Binary to execute
        *arguments: List of arguments to be passed to command
        valid_exit_codes: List of accepted exit codes from command
        raise_on_error: If True, de default, raises ProcessError if the exit codes isn't in valid_exit_codes

    Returns:
        Tuple with exitcode, stdout and stderr

    Raises:
        ProcessError: When the exit code isn't in valid_exit_codes
    """
    if not valid_exit_codes:
        valid_exit_codes = [0]
    LOGGER.debug("Executing %s %s", cmd, " ".join(args))
    proc = await asyncio.create_subprocess_exec(cmd, *args,
                                                stdout=stdout,
                                                stderr=stderr)
    out, err = await proc.communicate(stdin)
    if proc.returncode not in valid_exit_codes:
        msg = f"{cmd} returned exit code {proc.returncode}:\n{out}\n{err}"
        if raise_on_error:
            raise ProcessError(msg)
        LOGGER.debug(msg)
    return proc.returncode, out, err


def kill(pid: int, sig: int, check: bool = False):
    """Sends sig signal to pid.

    If check is True, returns True or False depending of the pid exists or not

    Args:
        pid: PID to kill or check
        sig: Signal to send to PID
        check: If True, we don't send the signal, only check if it exists

    Returns:
        If check is True, returns True if the process exists, False otherwise
    """
    try:
        os.kill(pid, 0)
    except OSError:
        LOGGER.debug("PID %d doesn't exist", pid)
        if check:
            return False
    else:
        if check:
            return True
        os.kill(pid, sig)
    return None
