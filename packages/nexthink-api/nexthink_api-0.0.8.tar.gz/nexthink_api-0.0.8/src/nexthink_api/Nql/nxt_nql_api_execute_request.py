"""NQL request class object."""
# ruff: noqa: N815 - Naming conforme to https://developer.nexthink.com/docs/api/nql-api/schemas/nql-api-execute-request


from typing import Annotated
from pydantic import BaseModel, Field


__all__ = ["NxtNqlApiExecuteRequest"]


class NxtNqlApiExecuteRequest(BaseModel):
    """Represent a NQL request object.

    Attributes:
    ----------
    queryId : str
        Identifier of the query which is going to be executed.
    parameters : dict[str, str]
        The parameters of the query.

    Note:
    ----
    The queryId is a string, with a maximum length of 255 characters,
    composed of alphanumeric characters (a-z, A-Z, 0-9), underscores (_),
    and start with a sharp character (#).

    The parameters is a dictionary of string keys and string values.

    """

    queryId: Annotated[
        str,
        Field(
            min_length=2,  # the sharp and at lest a character
            pattern=r'^#[a-z0-9_]{1,255}$'  # regex constraint
        )
    ]
    parameters: dict[str, str] = Field(default={})
