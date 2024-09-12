"""Nexthink API Object classes module. Based on Pydantic for data validation and serialization."""

from typing import Literal
from pydantic import BaseModel,  Field

__all__ = ["NxtSuccessResponse"]


class NxtSuccessResponse(BaseModel):
    """Response when ALL objects have been processed correctly.

    Attributes
    ----------
        status : Literal["success"]
            Indicate the success status of the response.

    """

    status: Literal["success"] = Field(default="success")
