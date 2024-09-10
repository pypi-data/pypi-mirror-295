# SPDX-FileCopyrightText: 2024 OpenBit
#
# SPDX-License-Identifier: MIT

"""Build images locally using QEMU

Uses QEMU to create a virtual machine to build images
"""
import asyncio
import logging
import os
import signal
import warnings

import aiofiles
import aiofiles.os
import aioshutil
import validators

from boxer import Builder
from boxer.common import download, execute, open_port, kill
from boxer.transport import SSH

LOGGER = logging.getLogger(__name__)


class Qemu(Builder):
    """Build images using QEMU

    Attributes:
        image_hash: String containing both the hash function and the hash of the image_url in the format of hash_function:hash
        image_url: URL to download the image. It can also be a path to a local file
        image_is_disk: If True, if value of image_url is a disk image to be used instead of a ISO image
        disk_size: Size of the final disk image
        disk_fomrat: Format of the final disk image
        disk_interface: QEMU interface to use to attach the disk
        cidata: Path to a directory that will be used as root of the CIDATA image
        uefi: If true (the default) will boot the VM in uefi mode
        ovmf_code_path: Path to OVMF code firmware
        ovmf_vars_path: Path to OVMF vars firmware
        qemu_executable: Name or path to the QEMU executable to be used
        qemu_args: List of adicional arguments to be passed to QEMU
        machine: QEMU machine to use
        accel: QEMU accelarator
        cpu: CPU model to use
        smp: Full SMP configurations
        memory: VM RAM
        vm_connection_port: Port where the target system is listening for remote commands. A forward is done to this port to be used by transport
        reboot_test_command: Command to use to detect system reboot. See notes on reboot method
    """
    image_hash = None
    image_url = None
    image_is_disk = False
    disk_size = "10G"
    disk_format = "qcow2"
    disk_interface = "virtio"
    cidata = None
    uefi = True
    ovmf_code_path = "/usr/share/OVMF/OVMF_CODE.fd"
    ovmf_vars_path = "/usr/share/OVMF/OVMF_VARS.fd"
    qemu_executable = "qemu-system-x86_64"
    qemu_args = []
    machine = "pc"
    accel = "tcg"
    cpu = "host"
    smp = "cpus=1,cores=2,threads=2,sockets=1,maxcpus=4"
    memory = "2048"
    vm_connection_port = 22
    _vnc_port = None
    reboot_test_command = "nc 127.0.0.1 22"

    @property
    def _required_binaries(self) -> list:
        return [self.qemu_executable, "qemu-img", "mkisofs"]

    @property
    def qemu_pid_file(self) -> str:
        """Returns the path where QEMU stores the VM pid"""
        return os.path.join(self.build_dir, "qemu.pid")

    @property
    def qemu_pid(self) -> str:
        """Returns the PID of the running VM"""
        if os.path.exists(self.qemu_pid_file):
            try:
                with open(self.qemu_pid_file, encoding="ascii") as pid:
                    return int(pid.read())
            except FileNotFoundError:
                pass
        return None

    @property
    def disk_path(self) -> str:
        """Returns the path to the disk"""
        return os.path.join(self.build_dir, "disk")

    @property
    def iso_path(self) -> str:
        """Returns the path to the ISO downloaded by image_url"""
        return os.path.join(self.build_dir, "iso")

    @property
    def cidata_path(self) -> str:
        """Returns the path of the CIDATA ISO"""
        return os.path.join(self.build_dir, "cidata")

    async def kill_qemu(self, req_sig: int = None) -> None:
        """Kill qemu process

        Sends a signal to the QEMU PID and waits to QEMU to exit
        By default, it sends SIGINT unless self.err is set where
        it sends the SIGKILL. The signal can be overriden by req_sig

        Args:
            req_sig: If provided, forces the signal to send to QEMU
        """
        pid = self.qemu_pid
        if pid and kill(pid, 0, True):
            LOGGER.info("Stopping qemu %s", f"with signal {req_sig.name}" if req_sig else "")
            sig = signal.SIGINT
            if req_sig:
                sig = req_sig
            elif self.err:
                sig = signal.SIGKILL
            while kill(pid, 0, True):
                kill(pid, sig)
                if sig != signal.SIGKILL:
                    await asyncio.sleep(1)
                else:
                    break
            await aiofiles.os.remove(self.qemu_pid_file)

    async def create_disk(self, path: str, size: str, disk_format: str) -> None:
        """Creates a new QEMU disk

        Calls qemu-img to create a new disk

        Args:
            path: Path to create the disk
            size: Size of the new disk
            dist_format: Format for the new disk
        """
        await execute("qemu-img", "create", "-f", disk_format, path, size)
        LOGGER.info("Created disk %s", path)

    async def resize_disk(self, path: str, size: str, disk_format: str) -> None:
        """Resizes a existing QEMU disk

        Calls qemu-img to resize a new disk

        Args:
            path: Path to the disk
            size: New size of the disk
            dist_format: Format for the disk
        """
        await execute("qemu-img", "resize", "-q", "-f", disk_format, path, size)
        LOGGER.info("Resized disk %s", path)

    async def create_cidata(self, path: str) -> None:
        """Creates CIDATA ISO

        Calls mkisofs to conver self.cidata_path to a ISO with the cidata label

        Args:
            path: Path to serve as root of the CIDATA ISO
        """
        if path:
            await execute("mkisofs", "-o", self.cidata_path, "-R", "-J", "-V", "cidata", path)
            LOGGER.info("Created CIDATA iso")

    async def test_connection(self, reader: asyncio.StreamReader, writer: asyncio.StreamWriter) -> bool:
        """Check if the VM is really accepting connections

        Because of the forward, the TCP connection between Transport and SSH is open
        but it doesn't mean that the OS is ready to handle.
        This checks if the target VM replies to the connection before calling
        upstream test_connection.

        Args:
            reader: asyncio.StreamReader object
            writer: asyncio.StreamWriter object

        Returns:
            True (from upstream) if the connection is valid, false otherwise.
        """
        if not isinstance(self.transport, SSH):
            warnings.warn("QEMU tests the connection by waiting for a reply from the server. This was only tested in SSH")

        # Will check if server replied with the client name and version
        # This is done because Qemu accepts the connection even if the
        # VM isn't accepting connections
        LOGGER.debug("Connection open. Reading output")
        data = None
        try:
            async with asyncio.timeout(1):
                data = (await reader.read(100)).decode()
        except TimeoutError:
            LOGGER.debug("Connection is open but no reply")

        if data:
            return await super().test_connection(reader, writer)
        return False

    # TODO: Check if reboot works with fixed upstream
    async def reboot(self, *a, **kw):  # pylint: disable=unused-argument
        """Reboot remote host

        For the same reason as test_connnection, we can't use the
        connection drop of transport to detect the reboot
        """
        async with self.transport.handle_interrupt():
            await self.run(self.reboot_command)
        try:
            await self.run(self.reboot_test_command)
        except:  # pylint: disable=bare-except # noqa: E722
            LOGGER.debug("Reboot test command failed. VM has rebooted")
        await self.wait_connection()

    async def prepare(self) -> None:
        """Prepares and starts the VM

        Builds QEMU arguments, creates all necessary files and starts the VM
        """
        await super().prepare()

        if self.uefi and (not await aiofiles.os.path.exists(self.ovmf_vars_path) or not await aiofiles.os.path.exists(self.ovmf_code_path)):
            raise ValueError("Cannot open OVMF files, required for UEFI.")

        if validators.url(self.image_url):
            local_path = (await download(alpine=(self.image_url, self.image_hash)))["alpine"]
        else:
            local_path = self.image_url

        if self.image_is_disk:
            LOGGER.info("Copying disk image")
            await aioshutil.copyfile(local_path, self.disk_path)
            await self.resize_disk(self.disk_path, self.disk_size, self.disk_format)
        else:
            await aiofiles.os.symlink(local_path, self.iso_path)
            await self.create_disk(self.disk_path, self.disk_size, self.disk_format)

        await self.create_cidata(self.cidata)

        self.transport.address = "127.0.0.1"
        self.transport.port = await open_port()
        self._vnc_port = await open_port(range_min=5900, range_max=6000)

        qemu_args = ["-machine", f"type={self.machine},accel={self.accel}", "-cpu", self.cpu, "-smp", self.smp, "-m", self.memory, "-name", self.uuid, "-uuid", self.uuid, "-drive", f"file={self.disk_path},if={self.disk_interface},media=disk,format={self.disk_format}", "-display", f"vnc=127.0.0.1:{5900 - self._vnc_port}", "-pidfile", self.qemu_pid_file, "-netdev", f"user,hostfwd=tcp:127.0.0.1:{self.transport.port}-:{self.vm_connection_port},id=forward", "-device", "virtio-net,netdev=forward,id=net0", "-daemonize"]

        if self.uefi:
            qemu_args.extend(["-drive", f"if=pflash,format=raw,readonly=on,file={self.ovmf_code_path}", "-drive", f"if=pflash,readonly=on,format=raw,file={self.ovmf_vars_path}"])
        if not self.image_is_disk:
            qemu_args.extend(["-drive", f"file={self.iso_path},media=cdrom"])
        if await aiofiles.os.path.exists(self.cidata_path):
            qemu_args.extend(["-drive", f"file={self.cidata_path},media=cdrom"])

        qemu_args.extend(self.qemu_args)

        await execute(self.qemu_executable, *qemu_args)

        LOGGER.info("QEMU will use port %d for VNC", self._vnc_port)
        LOGGER.info("QEMU will use port %d for remote connection", self.transport.port)

    async def finish(self):
        """Poweroff QEMU and copy the final files

        Sends the poweroff command and waits for QEMU process to stop.
        Then, copies the disk image and UEFI firmware (if running under UEFI) to the output directory
        """
        await super().finish()
        pid = self.qemu_pid
        while kill(pid, 0, True):
            LOGGER.info("Waiting for QEMU to stop")
            await asyncio.sleep(10)
        await aiofiles.os.mkdir(self.output_dir)
        async with asyncio.TaskGroup() as tg:
            tg.create_task(aioshutil.copy2(self.disk_path, os.path.join(self.output_dir, f"{self.build_name}.{self.disk_format}")))
            if self.uefi:
                tg.create_task(aioshutil.copy2(self.ovmf_code_path, self.output_dir))
                tg.create_task(aioshutil.copy2(self.ovmf_vars_path, self.output_dir))

    async def cancel(self):
        """Kills QEMU before running upstream cancel"""
        await self.kill_qemu(signal.SIGKILL)
        await super().cancel()

    async def cleanup(self):
        """Ensures that QEMU is killed"""
        await self.kill_qemu()
        await super().cleanup()
