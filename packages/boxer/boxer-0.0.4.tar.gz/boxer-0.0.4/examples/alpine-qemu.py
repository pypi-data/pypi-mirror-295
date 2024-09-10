# SPDX-FileCopyrightText: 2024 OpenBit
#
# SPDX-License-Identifier: MIT

import os

from boxer.builder import Qemu

import aiofiles
import aioshutil
import jinja2

METADATA ="""
hostname: {{hostname}}
local-hostname: {{hostname}}
public-keys:
  0=alpine:
  0:
    openssh-key: {{ssh_public_key}}
"""

class Alpine(Qemu):
    image_url = "https://dl-cdn.alpinelinux.org/alpine/v3.20/releases/cloud/nocloud_alpine-3.20.1-x86_64-uefi-tiny-r0.qcow2"
    image_hash = "sha512:b5b1a2307cf7ef4f874a32df9dea92266bdf3cfaa2cd1fe8256ca4654c1490ced4010d79ff91b3dbac12784a5ade965bd20d73fa4525788e01c81066dbc75bf5"
    image_is_disk = True
    cpu = "qemu64"
    qemu_args = ["-serial", "file:qemu.txt"]
    username = "alpine"
    poweroff_command = "doas /sbin/poweroff"

    async def create_cidata(self, path):
        async with aiofiles.tempfile.TemporaryDirectory() as tmp:
            template = jinja2.Environment(autoescape=True).from_string(METADATA)
            output = template.render(hostname="alpine-demo", ssh_public_key=self.transport.client_key.export_public_key().decode("ascii"))
            del template
            with open(os.path.join(tmp, "meta-data"), "w") as meta:
                meta.write(output)
            await super().create_cidata(tmp)

    async def build(self):
        async with aiofiles.tempfile.NamedTemporaryFile("w") as f:
            await f.write("touch /tmp/dummy")
            await f.seek(0)

            await self.copy(f.name, "test.sh")
            await self.run("/bin/sh", "test.sh")
