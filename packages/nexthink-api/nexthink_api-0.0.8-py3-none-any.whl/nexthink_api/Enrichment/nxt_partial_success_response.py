"""Partial success response when some of the objects in the request contain errors but other objects are processed."""

from typing import Literal
from pydantic import BaseModel, Field, conlist

from nexthink_api.Enrichment.nxt_individual_object_error import NxtIndividualObjectError

__all__ = ["NxtPartialSuccessResponse"]


# Note: NxtSuccessResponse already inherits from BaseModel
class NxtPartialSuccessResponse(BaseModel):
    """Partial success response when some of the objects in the request contain errors but other objects are processed.

    Attributes
    ----------
        status  : Literal["partial_success"]
            Indicates the status of the response as 'partial_success'.
        errors : list[NxtIndividualObjectError]
            List containing NxtIndividualObjectError instances representing the errors in the request.

    """

    status: Literal["partial_success"] = Field(default="partial_success")
    errors: conlist(NxtIndividualObjectError, min_length=1)
