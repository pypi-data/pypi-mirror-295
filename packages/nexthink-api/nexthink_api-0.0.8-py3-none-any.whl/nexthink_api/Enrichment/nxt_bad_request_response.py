"""Error response when ALL objects in the request contain errors."""

from typing import Literal
from pydantic import BaseModel, conlist, Field


from nexthink_api.Enrichment.nxt_individual_object_error import NxtIndividualObjectError

__all__ = ["NxtBadRequestResponse"]


class NxtBadRequestResponse(BaseModel):
    """Error response when ALL objects in the request contain errors.

    Attributes
    ----------
    status : Literal
        Literal value "error" representing the status of the response.
    errors : list[NxtIndividualObjectError]
        List containing NxtIndividualObjectError instances with a minimum length of 1.

    """

    status: Literal["error"] = Field(default="error")
    errors: conlist(NxtIndividualObjectError, min_length=1)
