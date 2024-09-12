"""Error when authentication has failed."""

from pydantic import BaseModel, Field

__all__ = ["NxtInvalidTokenRequest"]


class NxtInvalidTokenRequest(BaseModel):
    """Error when authentication has failed.

    Attributes
    ----------
        code: str
            Error code
        message: str
            Message with the description of the error

    """

    code: str = Field(min_length=1, default=401)
    message: str = Field(min_length=1, default="Unauthorized - invalid authentication credentials")
