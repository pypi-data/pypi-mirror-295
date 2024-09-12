"""Nexthink API Call Point List."""

from typing import Final, Optional
from enum import Enum


class NxtEndpoint(str, Enum):
    """Endpoint list of the Nexthink API."""

    Enrichment: Final[str] = '/api/v1/enrichment/data/fields'
    Act: Final[str] = '/api/v1/act/execute'
    Engage: Final[str] = '/api/v1/euf/campaign/trigger'
    Workflow: Final[str] = '/api/v1/workflow/execute'
    Nql: Final[str] = '/api/v1/nql/execute'
    NqlV2: Final[str] = '/api/v2/nql/execute'
    NqlExport: Final[str] = '/api/v1/nql/export'
    NqlStatus: Final[str] = '/api/v1/nql/status'
    Token: Final[str] = '/api/v1/token'

    @classmethod
    def get_api_name(cls, path: str) -> Optional[str]:
        """Get the API name from the path.

        Parameters
        ----------
            path : str
                path to the API.

        Returns
        -------
            Optional[str]
                The name of the API or None if path is not in the Endpoints list.

        """
        return next((endpoint.name for endpoint in cls if path.startswith(endpoint.value)), None)
