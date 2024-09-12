"""An error composed of a message and a code."""

from pydantic import BaseModel, Field

__all__ = ["NxtError"]


class NxtError(BaseModel):
    """hold an Error with a message and a code.

    Attributes
    ----------
    message: str
        Message with the description of the error
    code: str
        Error code

    """

    message: str = Field(min_length=1)
    code: str = Field(min_length=1)
