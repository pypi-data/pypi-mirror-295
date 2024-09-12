"""An error response for NQL request."""

from typing import Optional
from pydantic import BaseModel

__all__ = ["NxtErrorResponse"]


class NxtErrorResponse(BaseModel):
    """An error response for NQL request.

    Attributes
    ----------
        message: str
            Message with the description of the error
        code: int
            Error code
        source: Optional[str]
            Source of the error, if any

    """

    message: str
    code: int
    source: Optional[str] = None
