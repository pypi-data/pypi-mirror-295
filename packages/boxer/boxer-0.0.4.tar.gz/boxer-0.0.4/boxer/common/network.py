# SPDX-FileCopyrightText: 2024 OpenBit
#
# SPDX-License-Identifier: MIT

"""
Common network functions
"""
import asyncio
import hashlib
import logging
import os
import socket

import aiohttp
import aiofiles

from .constants import DOWNLOAD_PATH

LOGGER = logging.getLogger(__name__)
OPENPORT_LOCK = asyncio.BoundedSemaphore()


async def download(**kw) -> dict:
    """Downloads multiples files into the cache directory

    Arguments name will identify the download on the resulting dict.
    The values must be a tuple with the URI and the checksum, where
    the checksum has the following format: <checksum algorithm>:<checksum_hash>

    Args:
        **kw: Each named argument is a tuple containing the URI and a string with checksum hash function and hash.
                The hash string should be in the format <hash function>:<hash>

    Returns:
        A dictionary where the keys are the named arguments and the value the path to the downloaded file
    """
    async def _do(session, cache_key, url, checksum):
        if checksum:
            checksum_alg, checksum_hash = checksum.split(":")
            hsh = hashlib.new(checksum_alg)
        else:
            checksum_alg, checksum_hash, hsh = None, None, None
        path = os.path.join(DOWNLOAD_PATH, cache_key)

        if os.path.exists(path):
            cached = False
            if checksum_hash is None:
                cached = True
            else:
                async with aiofiles.open(path, "rb") as cached:
                    content = await cached.read()

                hsh.update(content)
                if hsh.hexdigest() == checksum_hash:
                    cached = True
            if cached:
                LOGGER.info("Download already cached")
                return
            LOGGER.warning("Cached hash doesn't match. Will force download")

        async with aiofiles.open(path, "w+b") as out:
            LOGGER.info("Downloading %s", url)
            resp = await session.get(url)
            await out.write(await resp.read())
            await out.seek(0)
            content = await out.read()

        if hsh:
            hsh.update(content)
        if checksum_hash is not None and hsh.hexdigest() != checksum_hash:
            raise ValueError("Provided checksum doesn't match")

    if not await aiofiles.os.path.exists(DOWNLOAD_PATH):
        await aiofiles.os.makedirs(DOWNLOAD_PATH)

    res = {}
    ct_name = asyncio.current_task().get_name()
    async with aiohttp.ClientSession() as session:
        async with asyncio.TaskGroup() as tg:
            for key, data in kw.items():
                uri, checksum = data
                cache_key = hashlib.sha256(uri.encode()).hexdigest()
                tg.create_task(_do(session, cache_key, uri, checksum), name=ct_name)
                res[key] = os.path.join(DOWNLOAD_PATH, cache_key)
    return res


async def open_port(family=socket.AF_INET, sock_type=socket.SOCK_STREAM, range_min: int = 0, range_max: int = 1) -> int:
    """Gets an available network port

    By default it will return a random port provided by the OS

    Args:
        family: Socket family to use
        sock_type: Type of socket to test the port availability
        range_min: Start of range of ports to get
        range_max: End of range of ports to get

    Returns:
        Port be used
    """
    async with OPENPORT_LOCK:
        sock = socket.socket(family, sock_type)
        for p in range(range_min, range_max + 1):
            if range_max == range_max + 1:
                raise OSError(f"Unable to alocate port between range {range_min} and {range_max}")
            if p in open_port.used_ports:
                LOGGER.debug("Port %d already in use", p)
                continue
            try:
                sock.bind(("", p))
                break
            except OSError:
                pass
        port = sock.getsockname()[1]
        sock.close()
        open_port.used_ports.append(port)
    return port
open_port.used_ports = []
