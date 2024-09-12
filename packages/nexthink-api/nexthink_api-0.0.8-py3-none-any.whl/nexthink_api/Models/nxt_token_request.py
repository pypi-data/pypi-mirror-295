"""Authentication request on the Nexthink API."""

from typing import Dict
from pydantic import BaseModel, Field


class NxtTokenRequest(BaseModel):
    """Model for an OAuth Authentication request on the Nexthink API.

    Attributes
    ----------
        data (Dict[str, str]):
            Header for requesting the Token

    """

    data: Dict[str, str] = Field(default={'grant_type': 'client_credentials'}, frozen=True)

    def get_request_header(self) -> dict:
        """Return the header for requesting the token.

        Returns
        -------
            dict(str, str):
                Header for requesting the Token

        """
        return self.data
