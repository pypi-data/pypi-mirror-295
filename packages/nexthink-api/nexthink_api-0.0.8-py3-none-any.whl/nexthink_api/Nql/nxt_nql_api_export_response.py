"""Class for the NQL API export response.

Export identifier to be used in the "status" operation to know the state
of the export and to retrieve the URL of the file with the results.
"""
# ruff: noqa: N815 - Naming conforme to https://developer.nexthink.com/docs/api/nql-api/schemas/nql-api-export-response


from typing import Annotated
from pydantic import BaseModel, Field

__all__ = ["NxtNqlApiExportResponse"]


class NxtNqlApiExportResponse(BaseModel):
    """Class for the NQL API export response.

    Attributes
    ----------
    exportId : str
        Identifier of the query which is going to be executed.

    """

    exportId: Annotated[
        str,
        Field(
            min_length=1
        )
    ]
