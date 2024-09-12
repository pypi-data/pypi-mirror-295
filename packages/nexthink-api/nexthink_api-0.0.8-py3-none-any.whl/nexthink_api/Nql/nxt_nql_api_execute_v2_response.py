"""NQL Class answer object for NQL request with V2 date format."""
# ruff: noqa: N815 - Naming conforme to
# https://developer.nexthink.com/docs/api/nql-api/schemas/nql-api-execute-v2-response

from datetime import datetime
from typing import List
from pydantic import BaseModel, field_validator

__all__ = ["NxtNqlApiExecuteV2Response"]


class NxtNqlApiExecuteV2Response(BaseModel):
    """NQL API execute V2 response.

    Attributes
    ----------
    queryId : str
        Identifier of the executed query.
    executedQuery : str
        Final query executed with the replaced parameters.
    rows : int
        Number of rows returned
    executionDateTime : str
        Date and time of the execution in ISO 8601 format (YYYY-MM-DDThh:mm:ss.sssTZD).
    data : List[dict[str, str]]
        List of dictionaries representing the rows of the query result.

    """

    queryId: str
    executedQuery: str
    rows: int
    executionDateTime: str
    data: List[dict[str, str]]

    # Avoid pycharm false positive
    # noinspection PyNestedDecorators
    @field_validator('executionDateTime')
    @classmethod
    def parse_execution_datetime(cls, value: str) -> str:
        """Parse the execution date time from ISO 8601 format (YYYY-MM-DDThh:mm:ss.sssTZD).

        Parameters
        ----------
            value (str): Value to be parsed.

        Returns
        -------
            str: Parsed datetime object.

        Raises
        ------
            ValueError: If the value is not in ISO 8601 format.

        """
        datetime.fromisoformat(value)
        return value
