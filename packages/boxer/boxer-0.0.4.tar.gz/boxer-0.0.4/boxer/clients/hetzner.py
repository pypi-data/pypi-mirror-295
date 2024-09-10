# SPDX-FileCopyrightText: 2024 OpenBit
# SPDX-FileContributor: Hugo Rodrigues
#
# SPDX-License-Identifier: MIT

"""
Hetzner API client
"""

import asyncio
import json
import logging

import aiohttp

from boxer import __version__
from boxer.common import exceptions

LOGGER = logging.getLogger(__name__)


class Hetzner():
    """HTTP Client to integrate with Hetzner

    Attributes:
        token: Hetzner authentication token
        base_url: URI that is common with all requests
        action_poll_wait_time: How much time to wait between actions updates
        api_version: Version of the Hetzner API. We only support v1
    """

    def __init__(self, token, base_url="https://api.hetzner.cloud", action_poll_wait_time=5, api_version=1):
        self.token = token
        if base_url[-1] == "/":
            base_url = base_url[:-1]
        self.base_url = base_url
        self.action_poll_wait_time = action_poll_wait_time
        self.api_version = 1
        self._session = None
        if api_version != 1:
            raise exceptions.BoxerException("We only support version 1 of the Hetzner API")

    async def __aenter__(self):
        session_headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.token}",
            "User-Agent": f"boxer/{__version__}"
        }
        self._session = aiohttp.ClientSession(headers=session_headers)
        return self

    async def __aexit__(self, exc_type, exc, tb):
        if not isinstance(exc_type, exceptions.MissingHTTPSession):
            await self._session.close()
        self._session = None

    def _get_full_url(self, path: str) -> str:
        """Build the endpoint full URL using the base_url, api_version and path

        Args:
            path: Endpoint part of the URL

        Returns:
            String with the full URL
        """
        if path[0] == "/":
            path = path[1:]
        return f"{self.base_url}/v{self.api_version}/{path}"

    @property
    def session(self) -> aiohttp.ClientSession:
        """Check if a HTTP session exists and returns if true

        Returns:
            aiohttp.ClientSession

        Raises:
            MissingHTTPSession if session doesn't exists
        """

        if isinstance(self._session, aiohttp.ClientSession):
            return self._session
        raise exceptions.MissingHTTPSession("HTTP session not created")

    async def request(self, method: str, path: str, *a, wait_for_action: bool = True, expected_status: list = None, **kw) -> dict:
        """Performs a request to Hetzner API.

        The signature of the method is the same as aiohttp.ClientSession.request except
        for the following arguments

        Args:
            wait_for_action: If true, wait for any action returned by the API
            expected_status: If the return status isn't on the list, a HTTPException is raised

        Returns:
            dict representing the API response

        Raises:
            HTTPException if return status not present in expected_status
        """
        if expected_status is None:
            expected_status = [200, 201, 204]
        url = self._get_full_url(path)
        LOGGER.debug("Calling Hetzner API: %s %s", method.upper(), url)
        res = await self.session.request(method, url, *a, **kw)
        try:
            response = await res.json()
        except (aiohttp.ContentTypeError, json.decoder.JSONDecodeError):
            if method != "delete":
                LOGGER.exception("Unable to parse API response")
            response = {}
        if res.status not in expected_status:
            error_code = response.get("error", {}).get("code", "NA")
            error_message = response.get("error", {}).get("message", "NA")
            raise exceptions.HTTPException(f"Got a HTTP error with status {res.status}, code {error_code} and message {error_message}")

        # Wait for any resulting action to finish
        if wait_for_action and "action" in response:
            LOGGER.debug("waiting for action %d that came from %s", response["action"]["id"], url)
            await self.wait_action(response["action"]["id"])

            # Special case for create server
            for action in response.get("next_actions", []):
                LOGGER.debug("waiting for action %d that came from %s", response["action"]["id"], url)
                await self.wait_action(action["id"])
        return response

    async def get(self, path: str, *a, **kw) -> dict:
        """Call self.request with method get

        This function as the same assinature as self.request
        """
        return await self.request("get", path, *a, **kw)

    async def post(self, path: str, *a, **kw) -> dict:
        """Call self.request with method post

        This function as the same assinature as self.request
        """
        return await self.request("post", path, *a, **kw)

    async def put(self, path: str, *a, **kw) -> dict:
        """Call self.request with method put

        This function as the same assinature as self.request
        """
        return await self.request("put", path, *a, **kw)

    async def delete(self, path: str, *a, **kw) -> dict:
        """Call self.request with method delete

        This function as the same assinature as self.request
        """
        return await self.request("delete", path, *a, **kw)

    async def wait_action(self, action_id: int, raise_on_error: bool = True) -> bool:
        """Blocks task until Hetzner action is complete

        Args:
            actiond_id: ID of the action
            raise_on_error: If True (default) will raise an exception when an error is detected

        Returns:
            True if action is completed with success. False otherwise

        Raises:
            HTTPException: Error processing action
        """
        action = {"action": {"status": "unknown"}}
        while action["action"]["status"] in ("running", "unknown"):
            LOGGER.debug("Action %s (ID: %d) is in state %s", action["action"].get("command", ""), action_id, action["action"]["status"])
            if action["action"]["status"] != "unknown":
                LOGGER.info("Waiting for action %s (id: %d) to end", action["action"]["command"], action_id)
                await asyncio.sleep(self.action_poll_wait_time)
            try:
                action = await self.get(f"actions/{action_id}", wait_for_action=False)
            except exceptions.HTTPException:
                if raise_on_error:
                    raise

        if action["action"]["status"] == "error":
            msg = f"Hetzner action action['action']['command'] (id: {action_id}) failed with {action['action']['error']['code']}: {action['action']['error']['message']}"
            if raise_on_error:
                raise exceptions.HTTPException(msg)
            LOGGER.error(msg)
            return False
        return True
