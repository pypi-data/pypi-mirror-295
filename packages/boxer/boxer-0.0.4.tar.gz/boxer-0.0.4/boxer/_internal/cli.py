# SPDX-FileCopyrightText: 2024 OpenBit
#
# SPDX-License-Identifier: MIT

"""Classes and functions used by the CLI"""

import asyncio
import argparse
import logging
import sys

from .version import VERSION

LOGGER = logging.getLogger(__name__)

ECODE_UNKNOWN_COMMAND = 249
ECODE_UNKNOWN_ERROR = 250


class CommandType(type):
    """
    Abstract class that gathers all commands
    """
    def __init__(cls, name, bases, attrs):
        super(CommandType, cls).__init__(name, bases, attrs)
        cls.name = getattr(cls, name, cls.__name__.lower())

    @staticmethod
    def get_commands():
        """Get all available command classes"""
        return {c.name: c.alias if c.alias else c for c in Command.__subclasses__()}


class Command(CommandType("Command", (object,), {"hidden": False, "alias": None, "name": None})):
    """
    Abstract class for normal CLI commands. Each command must implement run

    Attributes:
        hidden: If True, the command this hidden from the commands command unless --hidden is passed
        alias: An alias command is a command that uses another command. This should be a Command class
        name: Name of the command. By default is the lower case version of the class name
    """
    def __init__(self):
        self.parser = argparse.ArgumentParser()

        # NB: self.name is set by CommandType.__init__
        self.parser.prog = self.name  # pylint: disable=no-member
        if self.__doc__:
            self.parser.description = self.__doc__
        self.cli = None

    async def run(self) -> int:
        """
        This method must be implemented by each commmand. It's called by main
        If it's a async coroutine, it is called from inside a async loop
        """
        raise NotImplementedError("run method must be implemented be each command")

    def setup_parser(self):
        """Commands can use this method to add custom arguments"""

    def setup_cli(self, args):
        """
        Setup argparser.

        Args:
            args: List of CLI arguments to be parsed into setup parser
        """
        self.parser.add_argument("--verbose", dest="verbose", help="Show debug information", action="store_true")
        self.parser.add_argument("--version", dest="version", help="Show version", action="store_true")
        self.setup_parser()
        self.cli = self.parser.parse_args(args)


class Commands(Command):
    """Show all available commands"""
    hidden = True

    async def run(self):
        sys.stdout.write("Available commands:\n")
        padding = max(len(k.name) for k in Command.__subclasses__()) + 2
        for cmd in sorted(Command.__subclasses__(), key=lambda x: x.name):
            # Don't show hiddent commands, except if --hidden is passed
            if (self.cli is None or not self.cli.hidden) and cmd.hidden:
                continue
            name = cmd.name.ljust(padding, " ")
            doc = (cmd.__doc__ or "").strip()
            sys.stdout.write(f"    {name}{doc}\n")
        sys.stdout.write("\nUse '<command> --help' for full help.\n")

    def setup_parser(self):
        self.parser.add_argument("--hidden", dest="hidden", help="Include hidden commands", action="store_true")


async def _main(cmd):
    """Sets first task name to Main"""
    asyncio.current_task().set_name("Main")
    return await cmd.run()


def main():
    """Application entrypoint

    It parses the command to execute, calls setup_cli of the command
    and then runs the run method.
    It then returns of value returned by run
    """
    res = ECODE_UNKNOWN_ERROR
    ecode = None
    try:

        args = sys.argv[1:]

        command = None

        # Select command and check if it's valid
        if args and not args[0].startswith("-"):
            command = args[0]
            args = args[1:]

        if command not in CommandType.get_commands():
            if command is not None:
                sys.stderr.write(f"Unknown command {command}.\n\n")
                ecode = ECODE_UNKNOWN_COMMAND
            command = "commands"

        # Create command object
        cmd = CommandType.get_commands()[command]()
        cmd.setup_cli(args)

        if cmd.cli.version:
            print(VERSION)
            return 0

        # Actual application start
        LOGGER.debug("Starting %s", cmd.name)
        res = asyncio.run(_main(cmd))
        LOGGER.debug("%s returned %d", cmd.name, res if res else 0)
    except KeyboardInterrupt:
        res = 0
    return ecode if ecode else res
