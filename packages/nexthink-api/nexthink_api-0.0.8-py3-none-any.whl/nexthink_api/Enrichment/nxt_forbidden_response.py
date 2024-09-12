"""Error response when no permissions."""

from pydantic import BaseModel

__all__ = ["NxtForbiddenResponse"]


class NxtForbiddenResponse(BaseModel):
    """Error response when no permissions.

    Attributes
    ----------
    message : str
        Message describing the error.

    """

    message: str
