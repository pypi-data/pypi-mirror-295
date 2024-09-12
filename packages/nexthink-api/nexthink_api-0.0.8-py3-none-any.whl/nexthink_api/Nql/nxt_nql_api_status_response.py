"""NQL Status response for export request."""
# ruff: noqa: N815 - Naming conforme to https://developer.nexthink.com/docs/api/nql-api/schemas/nql-api-status-response

from typing import Optional
from pydantic import BaseModel, HttpUrl, field_serializer

from nexthink_api.Nql.nxt_nql_status import NxtNqlStatus

__all__ = ["NxtNqlApiStatusResponse"]


class NxtNqlApiStatusResponse(BaseModel):
    """Response status of an NQL API request.

    Attributes
    ----------
        status : NxtNqlStatus
            Status of the NQL API request.
        resultsFileUrl : Optional[HttpUrl]
            URL of the file with the content once the export has been completed.
        errorDescription : Optional[str]
            Message with the description of the error.

    """

    status: NxtNqlStatus
    resultsFileUrl: Optional[HttpUrl] = None
    errorDescription: Optional[str] = None

    @field_serializer('status', when_used='json')
    def serialize_status(self, value: NxtNqlStatus) -> str:
        """Serialize the status attribute to its value when used in JSON format.

        Parameters
        ----------
            value : NxtNqlStatus
                Value to be serialized.

        Returns
        -------
            str
                Serialized value of the status attribute.

        """
        return value.value
