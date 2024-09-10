# SPDX-FileCopyrightText: 2024 OpenBit
#
# SPDX-License-Identifier: MIT

"""Base transport class

Each transport method should inherit this class
"""
import asyncio
import contextlib
import logging

LOGGER = logging.getLogger(__name__)


class Transport():
    """Base transport class

    Attributes:
        address: Build IP address used to connect into it
        port: Build port used to connect into it
        username: Username used to login into the build
        password: Password used to login into the build
    """
    address = None
    port = None
    username = None
    password = None

    def __init__(self):
        self._shared_cn = None

    @contextlib.asynccontextmanager
    async def shared_connection(self) -> None:
        """Context manager to manage a shared connection

        This is usefull to run multiple commands without needing
        to open a close multiple connections. The shared connection is
        stored on self._shared_cn.

        Each transport should check if self._shared_cn is not None and
        yield it if true
        """
        if self._shared_cn is not None:
            raise ValueError("An existing shared connection is already active")
        try:
            async with self.connect() as cn:
                self._shared_cn = cn
                yield
        finally:
            self._shared_cn = None

    @contextlib.asynccontextmanager
    async def connect(self):
        """Connects to the transport

        This method must be implemented by each transport

        Raises:
            NotImplementedError: When a transport doesn't implement the method
        """
        raise NotImplementedError("connect must be implemented by each transport")

    async def run(self, command: str, *arguments: any, valid_exit_codes: list = None, raise_on_error: bool = True) -> tuple:
        """Runs a command inside the build machine

        This method must be implemented by each transport

        Args:
            command: Binary to execute
            *arguments: List of arguments to be passed to command
            valid_exit_codes: List of accepted exit codes from command
            raise_on_error: If True, de default, raises ProcessError if the exit codes isn't in valid_exit_codes

        Returns:
            Tuple with exitcode, stdout and stderr

        Raises:
            NotImplementedError: When a transport doesn't implement the method
        """
        raise NotImplementedError("run must be implemented by each transport")

    @contextlib.asynccontextmanager
    async def handle_interrupt(self):
        """Context manager that catches a connection drop

        This method must be implemented by each transport

        Raises:
            NotImplementedError: When a transport doesn't implement the method
        """
        raise NotImplementedError("handle_interrupt must be implemented by each transport")

    async def copy(self, source: str, destination: str, reverse: bool = False, recurse: bool = False):
        """Copy files/directories between host and build machines

        This method must be implemented by each transport

        Args:
            source: Path of the file/directory to be copied
            destination: Where to store the copied file/directory
            reverse: If True, copies the file from the build machine to the local host
            recurse: If True, copy all child contents of the directory

        Raises:w
            NotImplementedError: When a transport doesn't implement the method
        """
        raise NotImplementedError("copy must be implemented by each transport")

    async def test_connection(self, reader: asyncio.StreamReader, writer: asyncio.StreamWriter) -> bool:  # pylint: disable=unused-argument
        """Test connection to the target build

        This should be implemented by each transport if a more advance check is required

        Args:
            reader: asyncio.StreamReader instance
            writer: asyncio.StreamWriter instance

        Returns:
            No real test is done, so always True
        """
        return True

    async def wait_connection(self, callback=None) -> None:
        """Wait for transport address and port are open

        It opens a TCP connection and then calls callback if it's set
        Only exists when the connection is open and test_connection returns True

        Args:
            callback: async coroutine that will test if the open connection is valid
        """
        connected = False

        if not self.address or not self.port:
            raise ValueError("Connection address and/or port not set")
        while not connected:
            sleep = True
            try:
                LOGGER.info("Trying connection to %s:%d", self.address, self.port)
                async with asyncio.timeout(10):
                    reader, writer = await asyncio.open_connection(self.address, self.port)

                try:
                    if callable(callback):
                        connected = await callback(reader, writer)
                    else:
                        connected = True
                finally:
                    writer.close()
                    await writer.wait_closed()
            except TimeoutError:
                sleep = False
                LOGGER.debug("Connection time out")
            except (ConnectionRefusedError, OSError):
                LOGGER.debug("Connection refused")
            if not connected and sleep:
                await asyncio.sleep(10)
        LOGGER.info("%s connection available", self.__class__.__name__)
