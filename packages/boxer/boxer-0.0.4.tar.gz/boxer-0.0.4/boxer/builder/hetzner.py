# SPDX-FileCopyrightText: 2024 OpenBit
#
# SPDX-License-Identifier: MIT

"""Build images on Hetzner

Uses Hetzner API to create a instance and then to create a snapshot
"""

import asyncio
import contextlib
import logging
import os

from boxer import Builder, clients
from boxer.common import exceptions
from boxer.transport import SSH

LOGGER = logging.getLogger(__name__)


class Hetzner(Builder):
    """Build images on Hetzner

    Attributes:
        token: Hetzner authentication token. Value is taken from HCLOUD_TOKEN environment variable if not set
        name: Name of the image to be build. If not set, build_name is used
        labels: Labels to apply to the image
        protect: If true, enable protection of the image
        image: Base image to build from
        architecture: Architecture of the image
        server_type: Server type to be used during the build
        location: Location used during the build
        port: Transport port
        username: Transport username
        password: Transport password
    """
    token = os.environ.get("HCLOUD_TOKEN", None)
    name = None
    labels = None
    protect = False
    image = None
    architecture = "x86"
    server_type = None
    location = None
    port = 22
    username = "root"
    password = None
    _boxer_ssh_key = None
    _boxer_server = None

    def __init__(self, *a, **kw):
        if self.name is None:
            self.name == self.build_name  # pylint: disable=pointless-statement
        super().__init__(*a, **kw)

    async def _get_server(self, client):
        if self._boxer_server is None:
            raise exceptions.BoxerException("Server not created yet")
        return await client.get(f"servers/{self._boxer_server}")

    @contextlib.asynccontextmanager
    async def client(self):
        """Context manager to open an Hetzner client"""
        async with clients.Hetzner(self.token) as client:
            yield client

    async def prepare(self):
        await super().prepare()
        async with self.client() as client:
            server_args = {
                "image": self.image,
                "name": f"boxer-{self.uuid}",
                "server_type": self.server_type,
                "location": self.location
            }

            if isinstance(self.transport, SSH):
                self._boxer_ssh_key = (await client.post("ssh_keys", json={"name": f"boxer-{self.uuid}", "public_key": self.transport.client_key.export_public_key().decode("ascii").splitlines()[0]}))["ssh_key"]["id"]
                server_args["ssh_keys"] = [self._boxer_ssh_key]

            server = await client.post("servers", json=server_args)
            self._boxer_server = server["server"]["id"]
            if server.get("root_password", None):
                self.password = server["root_password"]
                self.transport.password = self.password

            self.transport.port = self.port
            self.transport.address = server["server"]["public_net"]["ipv4"]["ip"]

    async def finish(self):
        await super().finish()
        async with self.client() as client:
            server = {"server": {"status": "unset"}}
            while server["server"]["status"] in ("running", "stopping", "unset"):
                if server["server"]["status"] != "unset":
                    LOGGER.info("Waiting for server to stop")
                    await asyncio.sleep(10)
                server = await self._get_server(client)
            if server["server"]["status"] != "off":
                raise exceptions.BoxerException(f"Inconsistent server status: {server['server']['status']}")

            LOGGER.info("Creating image")
            create_img_args = {
                "description": self.name,
                "type": "snapshot"
            }
            if self.labels:
                create_img_args["labels"] = self.labels
            image = await client.post(f"servers/{self._boxer_server}/actions/create_image", json=create_img_args)
            if self.protect:
                LOGGER.info("Protecting image")
                await client.post(f"images/{image['image']['id']}/actions/change_protection", json={"delete": True})

    async def cleanup(self):
        await super().cleanup()
        if self._boxer_server is not None:
            async with self.client() as client:
                server = await self._get_server(client)
                if server["server"]["status"] in ("running", "starting", "stopping"):
                    LOGGER.info("Forcing poweroff of server")
                    await client.post(f"servers/{self._boxer_server}/actions/poweroff")

                LOGGER.info("Deleting server")
                await client.delete(f"servers/{self._boxer_server}")
                if self._boxer_ssh_key:
                    LOGGER.info("Deleting temporary SSH key")
                    await client.delete(f"ssh_keys/{self._boxer_ssh_key}")
