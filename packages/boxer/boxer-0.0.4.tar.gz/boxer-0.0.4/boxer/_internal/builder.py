# SPDX-FileCopyrightText: 2024 OpenBit
#
# SPDX-License-Identifier: MIT

"""Base builder class

This class should be used to create new builder
"""
import asyncio
import importlib
import logging
import os
import pathlib
import signal
import shutil
import types
import uuid

import aioshutil

from boxer.common.constants import RE_MODULE_CLASS
from boxer.common.exceptions import RequiredBinaryError

LOGGER = logging.getLogger(__name__)


class Builder():
    """Base builders used to create builders

    Attributes:
        _required_binaries: List of binaries that a builder requires
        _signals: List of tuples with signal and callback used when signal is triggered
        transport: Transport class used to communicate with the image being built
        username: Username used to login into the image. Used by transport
        password: Password used to login into the image. Used by transport
        uuid: Build unique identifier
        poweroff_command: Command to run to poweroff remote system
        reboot_command: Command to run to reboot remote system
    """
    _required_binaries = []
    _signals = []
    transport = "boxer.transport.SSH"
    poweroff_command = "poweroff"
    reboot_command = "reboot"
    username = None
    password = None

    def __init__(self, variables: types.MappingProxyType, cli):
        self.uuid = str(uuid.uuid4())
        if os.path.exists(self.output_dir):
            raise FileExistsError(f"Output path {self.output_dir} already exists")
        self.variables = variables
        self.cleanup_build_dir = not cli.dont_clean
        self.err = None
        os.makedirs(self.build_dir)
        LOGGER.debug("Created build directory at %s", self.build_dir)

        for binary in self._required_binaries:
            if not shutil.which(binary):
                raise RequiredBinaryError(f"Missing required binary: {binary}")

        transport = RE_MODULE_CLASS.fullmatch(self.transport)

        transport_module_g = transport.group(1)
        transport_class_g = transport.group(2)

        if not transport_module_g or not transport_class_g:
            raise ImportError("Unable to get transport class")

        LOGGER.debug("Transport class %s from %s", transport_class_g, transport_module_g)

        try:
            transport_module = importlib.import_module(transport_module_g)
            transport_class = getattr(transport_module, transport_class_g)
        except AttributeError:
            LOGGER.error("Unable to import %s transport class from %s", transport_class_g, transport_module_g)
            raise
        except ModuleNotFoundError:
            LOGGER.error("Unable to import %s transport module", transport_module_g)
            raise

        self.transport = transport_class()
        self.transport.username = self.username
        self.transport.password = self.password

    @property
    def build_name(self) -> str:
        """Returns name of the build"""
        return self.__class__.__name__.lower()

    @property
    def output_dir(self):
        """Returns build output directory"""
        return f"output-{self.build_name}"

    @property
    def build_dir(self) -> str:
        """Returns building directory

        Can be used to store files required for the build
        """
        return os.path.join(pathlib.Path.home(), ".cache", "boxer", "build", self.uuid)

    async def prepare(self):
        """Prepares the build

        Register self._signals into the async loop.

        Builders should use this method to prepare the build
        before the build steps are executed
        """
        loop = asyncio.get_running_loop()

        # Add exit signals
        for sig in self._signals:
            if sig[0] in (signal.SIGINT, signal.SIGTERM):
                raise ValueError(f"{sig[0].name} is reserved")

            loop.add_signal_handler(sig[0], sig[1], loop, sig)

    async def test_connection(self, reader: asyncio.StreamReader, writer: asyncio.StreamWriter) -> bool:  # pylint: disable=unused-argument
        """Calls self.transport.test_connection

        Builders can also use this to perform adicional tests. Check QEMU builder as an example

        Returns:
            Whatever the connection is ready or not
        """
        return await self.transport.test_connection(reader, writer)

    async def wait_connection(self):
        """Wait for the connection to the build is available

        Builders should setup the transport connection details
        It calls self.transport.wait_connection with self.test_connection as a callback function
        """
        await self.transport.wait_connection(self.test_connection)

    async def reboot(self) -> None:
        """Sends a reboot command and waits for a new connection

        This method has the same signature as copy
        """
        LOGGER.info("Rebooting")
        async with self.transport.handle_interrupt():
            await self.run(self.reboot_command)
            while True:
                await self.run("", raise_on_error=False)
                LOGGER.debug("Waiting for connection drop due to reboot")
                await asyncio.sleep(30)
        await self.wait_connection()

    async def copy(self, *a, **kw) -> any:
        """Copy files between host and build.

        Check Transport.copy for more information
        """
        LOGGER.info("Copying file")
        return await self.transport.copy(*a, **kw)

    async def run(self, *a, **kw) -> any:
        """Runs a command inside the build.

        Check Transport.run for more information
        """
        LOGGER.info("Running shell command")
        return await self.transport.run(*a, **kw)

    async def build(self) -> None:
        """Steps to build the image

        Each build (not Builder) should implement this method
        to perform the desired provisioning
        """

    async def finish(self) -> None:
        """Sends the poweroff command to the build

        Builders and builds can also use this method to perform
        extra steps. Check QEMU builder for example.
        """
        LOGGER.info("Sending poweroff command")
        async with self.transport.handle_interrupt():
            await self.run(self.poweroff_command, valid_exit_codes=[None, 0])

    async def cancel(self) -> None:
        """Cancels a task

        Builders should use this method when the build is cancelled
        """

    async def cleanup(self) -> None:
        """Deletes the build directory

        Builders can also use this method to clean up any temporary resources that
        was created
        """
        if self.cleanup_build_dir:
            try:
                LOGGER.debug("Removing build directory")
                await aioshutil.rmtree(self.build_dir)
            except OSError:
                LOGGER.exception("Unable to remove build directory at %s", self.build_dir)

    async def error(self, err: Exception) -> None:
        """Registers the exception on self.err"""
        self.err = err
