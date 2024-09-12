"""NQL class answer object for V1 request."""
# ruff: noqa: N815 - Naming conforme to https://developer.nexthink.com/docs/api/nql-api/schemas/nql-api-execute-response

from pydantic import BaseModel, NonNegativeInt

from nexthink_api.Nql.nxt_date_time import NxtDateTime

__all__ = ["NxtNqlApiExecuteResponse"]


class NxtNqlApiExecuteResponse(BaseModel):
    """NQL Class answer object for V1 request.

    Parameters
    ----------
        queryId: str
            Identifier of the executed query.
        executedQuery: str
            Final query executed with the replaced parameters.
        rows: int
            Number of rows returned
        executionDateTime: NxtDateTime
            Date and time of the execution

    """

    queryId: str
    executedQuery: str
    rows: NonNegativeInt
    executionDateTime: NxtDateTime
    headers: list[str]
    data: list[list]
