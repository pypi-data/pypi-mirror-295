# SPDX-FileCopyrightText: 2024 OpenBit
# SPDX-FileContributor: Hugo Rodrigues
#
# SPDX-License-Identifier: MIT

"""Hetzner utilities"""

import logging

import aiofiles
import validators

from boxer import clients
from boxer.transport import SSH
from boxer.common import download

LOGGER = logging.getLogger(__name__)

# We store on /dev/shm because the rescue disk doesn't have a lot of space
REMOTE_LOCATION = "/dev/shm/image"  # nosec: B108


async def flash_from_image(token: str, server_id: int, image: str, checksum: str = None, is_qcow2: bool = False, callback: callable = None, remote_location: str = REMOTE_LOCATION) -> None:
    """Flash a qcow2 or raw image into the server disk

    Args:
        token: Hetzner token
        server_id: id of the server to be flashed
        image: URL or path of the image to flash
        checksum: Image checksum for validation. Used only the image is a URL
        is_qcow2: If true, will convert the image to raw format
        callback: Function to call before rebooting the server
        remote_location: Where to store the image on the server
    """

    if validators.url(image):
        image_path = (await download(image=(image, checksum)))["image"]
    else:
        image_path = image

    transport = SSH()
    transport.username = "root"
    transport.port = 22
    ssh_key_id = None

    async with clients.Hetzner(token) as client:
        try:
            server = await client.get(f"servers/{server_id}")
            if server["server"]["status"] in ("running", "starting", "stopping"):
                LOGGER.info("Forcing poweroff of server")
                await client.post(f"servers/{server_id}/actions/poweroff")

            transport.address = server["server"]["public_net"]["ipv4"]["ip"]

            ssh_key_id = (await client.post("ssh_keys", json={"name": "boxer-rescue", "public_key": transport.client_key.export_public_key().decode("ascii").splitlines()[0]}))["ssh_key"]["id"]

            await client.post(f"servers/{server_id}/actions/enable_rescue", json={"ssh_keys": [ssh_key_id]})
            await client.post(f"servers/{server_id}/actions/poweron")
            await transport.wait_connection(transport.test_connection)
            async with transport.shared_connection():
                await transport.copy(image_path, remote_location)
                async with aiofiles.tempfile.NamedTemporaryFile("w") as tmp:
                    await tmp.write("""#!/bin/sh
                                    set -ex""")
                    if is_qcow2:
                        await tmp.write(f"""
                        qemu-img convert -f qcow2 -O raw {remote_location} {remote_location}.img
                        dd if={remote_location}.img of=/dev/sda conv=fsync bs=1M
                        """)
                    else:
                        await tmp.write("""
                        dd if={remote_location} of=/dev/sda conv=fsync bs=1M
                        """)
                    await tmp.write("""
                                    sync""")
                    await tmp.flush()
                    await transport.copy(tmp.name, "/root/script.sh")
                await transport.run("/bin/sh", "/root/script.sh")
                if callable(callback):
                    await callback(transport)
            await client.post(f"servers/{server_id}/actions/disable_rescue")
            await client.post(f"servers/{server_id}/actions/reboot")

        finally:
            if ssh_key_id is not None:
                await client.delete(f"ssh_keys/{ssh_key_id}")
