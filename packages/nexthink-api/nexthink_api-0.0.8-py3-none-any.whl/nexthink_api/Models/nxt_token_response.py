"""Nexthink API Authentification answer."""

from typing import Annotated
from pydantic import BaseModel, Field


class NxtTokenResponse(BaseModel):
    """Nexthink API Token answer.

    Attributes
    ----------
        token_type : str
            The type of the token.
        expires_in : int
            The expiration time of the token.
        access_token str
            The access token.
        scope : str
            The scope of the token.

    """

    token_type: Annotated[str, Field(min_length=1)]
    expires_in: Annotated[int, Field(ge=0)]
    access_token: Annotated[str, Field(min_length=1)]
    scope: Annotated[str, Field(min_length=1)]
