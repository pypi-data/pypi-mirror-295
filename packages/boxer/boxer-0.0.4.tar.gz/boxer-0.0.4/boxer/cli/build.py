# SPDX-FileCopyrightText: 2024 OpenBit
#
# SPDX-License-Identifier: MIT

"""
The build command allows a user to build VMs based on a playbook
"""

import asyncio
import importlib.util
import itertools
import json
import logging
import os
import signal
import sys
import types

from boxer.common import kill
from boxer import Command, Builder

LOGGER = logging.getLogger(__name__)


class Build(Command):
    """
    Builds a VM image
    """

    def __init__(self):
        super().__init__()
        self.kill_called = 0

    def setup_parser(self):
        self.parser.add_argument("playbook", help="Playbook containing the build instructions")
        self.parser.add_argument("--var", metavar="variable", dest="variables", action="append",
                                 help="Set playbook variables", default=[])
        self.parser.add_argument("--only", metavar="image", dest="only", action="append",
                                 help="Limit the images to be run", default=[])
        self.parser.add_argument("--dont-clean", dest="dont_clean", action="store_true",
                                 help="Don't clean the build directory")

    async def process_builder(self, builder: any, variables: types.MappingProxyType) -> None:
        """Used to run a single build

        Args:
            builder: Builder class to execute
            variables: Extra variables set with --var cli argument
        """
        LOGGER.info("Processing builder %s", builder.__name__)
        build = builder(variables, self.cli)
        try:
            LOGGER.debug("Calling prepare")
            await build.prepare()
            LOGGER.debug("Calling wait_connection")
            await build.wait_connection()
            LOGGER.info("Starting build instructions")
            await build.build()
            LOGGER.debug("Calling finish")
            await build.finish()
        except asyncio.CancelledError:
            LOGGER.debug("Calling cancel")
            await build.cancel()
        except Exception as err:  # pylint: disable=broad-exception-caught
            LOGGER.exception("An error occured during processing")
            await build.error(err)
        finally:
            LOGGER.debug("Calling cleanup")
            await build.cleanup()

    def kill(self, signame, loop):
        """Cancel all builder tasks

        When called by the first time, sends a cancel command to all tasks.
        By the 3rd time outputs a warning informing the user that force cancelling can
        cuase builds not being cleaned
        By the 5th time, sends a SIGKILL to our selfs
        """
        self.kill_called += 1
        if self.kill_called == 1:
            LOGGER.error("Builds cancelled")
            for task in asyncio.all_tasks(loop):
                task.cancel(msg=f"Received {signame}")
        elif self.kill_called == 3:
            LOGGER.warning("Tried to kill builds multiple times. This can result in builds not being cleaned.")
        elif self.kill_called == 5:
            kill(os.getpid(), signal.SIGKILL)

    async def run(self) -> int:
        """Starts all builds, one per async task

        Parses the adicional variables passed via --var CLI argument.
        Loads the playbook (a Python file) to fetch all subclasses of used Builders
        """
        rwvar = {}
        for variable in self.cli.variables:
            splitted = variable.split("=")
            rwvar[splitted[0]] = "=".join(splitted[1:])
        variables = types.MappingProxyType(rwvar.copy())

        LOGGER.debug("Runtime variables:\n%s", json.dumps(rwvar, indent=2))
        del rwvar

        loop = asyncio.get_running_loop()

        # Add exit signals
        for sig in [signal.SIGINT, signal.SIGTERM]:
            # We recreat the signal since linting says that signal.SIGINT does't have name member
            loop.add_signal_handler(sig, self.kill, signal.Signals(sig).name, loop)

        spec = importlib.util.spec_from_file_location("boxer.playbook", self.cli.playbook)
        playbook = importlib.util.module_from_spec(spec)
        sys.modules["boxer.playbook"] = playbook
        spec.loader.exec_module(playbook)

        async with asyncio.TaskGroup() as tg:
            for builder in itertools.chain.from_iterable([x.__subclasses__() for x in Builder.__subclasses__()]):
                if self.cli.only and builder.__name__ not in self.cli.only:
                    continue
                tg.create_task(self.process_builder(builder, variables), name=builder.__name__)

        return 1 if self.kill_called > 0 else 0
