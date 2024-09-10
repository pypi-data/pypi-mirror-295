# SPDX-FileCopyrightText: 2024 OpenBit
#
# SPDX-License-Identifier: MIT

"""Transport for SSH connections

Used by default for every build, it allows you to communicate with
your build using SSH.
It generates a runtime SSH key-pair that can be used by cloud-init
like tools during the initial bootstrap of the OS.
"""
import asyncio
import contextlib
import logging

import asyncssh

from boxer import Transport
from boxer.common.exceptions import ProcessError

LOGGER = logging.getLogger(__name__)

asyncssh.set_log_level(logging.CRITICAL)
asyncssh.set_sftp_log_level(logging.CRITICAL)


class SSH(Transport):
    """Transport for SSH connections

    Attributes:
        host_key: SSH key fetched from the build machine
        username: Username used to login. Default value is root
        host_key_algorithms: List of algorithms that the build machine must support for the host key. Default values are ssh-rsa and ssh-ed25519.
        client_key_algorithm: Algorithm used to generate client key-pair. Default is ssh-ed25519
    """
    host_key = None
    _client_key = None
    username = "root"
    host_key_algorithms = ["ssh-rsa", "ssh-ed25519"]
    client_key_algorithm = "ssh-ed25519"

    @property
    def known_hosts(self) -> bytes:
        """Get an OpenSSH compatible known hosts encoded string with the host public key

        Returns:
            An OpenSSH compatible known hosts line. Examples:

            [1.2.3.4]:2224 ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAICnSOUO8u6SO+jwkooIZrGVGX2sN182631YOs2AU5T/b
            1.2.3.4 ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAICnSOUO8u6SO+jwkooIZrGVGX2sN182631YOs2AU5T/b

            Returned string is always ASCII encoded
        """
        if not self.host_key:
            raise ValueError("Please get the host key first")
        if self.port != 22:
            address = f"[{self.address}]:{self.port}"
        else:
            address = self.address
        return (f"{address} {self.host_key.export_public_key().decode('ascii')}").encode("ascii")

    async def test_connection(self, reader: asyncio.StreamReader, writer: asyncio.StreamWriter) -> bool:
        """Test SSH connection

        Tries to connect to the host

        Args:
            reader: asyncio.StreamReader instance
            writer: asyncio.StreamWriter instance

        Returns:
            Returns True if we are able to connect to the remote system. False otherwise.
        """
        try:
            async with self.connect():
                pass
        except (OSError, asyncssh.Error) as err:
            LOGGER.warning("Failed to open SSH connection to %s:%d: %s", self.address, self.port, str(err))
            return False
        return True

    async def get_host_key(self) -> asyncssh.SSHKey:
        """Get the SSH host key from the build machine

        Connects to the build machine and get the public host key. The key is then stored on self.host_key

        Returns:

            An instance of asyncssh.SSHKey with the public key.
        """
        if not self.host_key:
            self.host_key = await asyncssh.get_server_host_key(self.address, self.port, server_host_key_algs=self.host_key_algorithms)

        return self.host_key

    @property
    def client_key(self) -> asyncssh.SSHKeyPair:
        """Generate and returns a SSH key pair for authentication

        Returns:
            An instance of asyncssh.SSHKeyPeir
        """
        if not self._client_key:
            self._client_key = asyncssh.generate_private_key(self.client_key_algorithm)
        return self._client_key

    @contextlib.asynccontextmanager
    async def connect(self) -> asyncssh.SSHClientConnection:
        """Connect to the build machine

        Opens an SSH connection to self.address and self.port using self.username as the user and self.client_key as the SSH key

        Yields:
            An asycnssh.SSHClientConnection
        """
        if self._shared_cn:
            yield self._shared_cn
        else:
            await self.get_host_key()
            async with asyncssh.connect(host=self.address, port=self.port, username=self.username, known_hosts=self.known_hosts, client_keys=self.client_key) as cn:
                yield cn

    @contextlib.asynccontextmanager
    async def handle_interrupt(self):
        try:
            yield
        except (asyncssh.DisconnectError, asyncssh.ConnectionLost):
            LOGGER.info("SSH connection dropped")

    async def run(self, command: str, *arguments: any, valid_exit_codes: list = None, raise_on_error: bool = True) -> tuple:
        """Runs a SSH on the build machine

        Opens an SSH connections and runs the comand with arguments.
        It then returns the return code, stdout and stderr.

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
        cmd = f"{command} {' '.join(arguments)}"
        if not isinstance(valid_exit_codes, list):
            valid_exit_codes = [0]
        async with self.connect() as cn:
            LOGGER.debug("SSH: %s", cmd)
            result = await cn.run(cmd, check=False)
        if result.returncode not in valid_exit_codes:
            msg = f"remote {command} in returned exit code {result.returncode}:\n{result.stdout}\n{result.stderr}"
            if raise_on_error:
                raise ProcessError(msg)
            LOGGER.debug(msg)
        return result.returncode, result.stdout, result.stderr

    async def copy(self, source: str, destination: str, reverse: bool = False, recurse: bool = False) -> None:
        """Copy files/directories between host and build machines

        Files can be copied/directories either to or from the build machine.

        Args:
            source: Path of the file/directory to be copied
            destination: Where to store the copied file/directory
            reverse: If True, copies the file from the build machine to the local host
            recurse: If True, copy all child contents of the directory
        """
        # from VM to local
        async with self.connect() as cn:
            if reverse:
                src = (cn, source)
                dst = destination
            else:
                src = source
                dst = (cn, destination)
            await asyncssh.scp(src, dst, recurse=recurse)
