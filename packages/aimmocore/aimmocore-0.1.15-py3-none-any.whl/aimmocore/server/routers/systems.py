""" This module contains the system router for the aimmocore server. """

from starlette.responses import PlainTextResponse
from starlette.endpoints import HTTPEndpoint
from starlette.requests import Request
from aimmocore.core.utils import get_version


class VersionRouter(HTTPEndpoint):
    """Endpoint for exporting datasets to a file."""

    def get(self, request: Request):
        """Handles GET requests to get the aimmocore version info.

        Returns:
            str: aimmocore version info
        """
        return PlainTextResponse(get_version())
