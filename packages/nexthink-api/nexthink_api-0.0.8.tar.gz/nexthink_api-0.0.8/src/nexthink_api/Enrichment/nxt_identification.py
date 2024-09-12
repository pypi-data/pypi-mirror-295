"""Identification information for the given object, composed of the name of the field and the value used to identify."""

from typing import Union
from pydantic import BaseModel, field_serializer, field_validator, InstanceOf

from nexthink_api.Enrichment.nxt_identification_name import NxtIdentificationName

__all__ = ["NxtIdentification"]


class NxtIdentification(BaseModel):
    """IdentIdentification info for the given object, including the field name and its value.

    Attributes
    ----------
        name : NxtIdentificationName
            The name of the identification field.
        value : str
            The value used to identify the object.

    """

    name: InstanceOf[NxtIdentificationName]
    value: str

    @field_serializer('name', when_used='json')
    def name(self, value: NxtIdentificationName) -> str:
        """Serialize the 'name' field when used in JSON.

        Parameters
        ----------
        value : NxtIdentificationName
            Name of the field to be used to identify the object.

        Returns
        -------
            str
                string value of the name field

        """
        return value.value

    @field_validator('name', mode='before')
    @classmethod
    def validate_name(cls, value: Union[str, NxtIdentificationName]) -> NxtIdentificationName:
        """Convert value to NxtIdentification if needed.

        Parameters
        ----------
        value : Union [str, NxtIdentificationName]
            Name of the field to be used to identify the object.

        Returns
        -------
            NxtIdentificationName
                Name of the field to be used to identify the object.

        """
        if isinstance(value, str):
            return NxtIdentificationName(value)
        return value

    @field_validator('value')
    @classmethod
    def check_non_empty(cls, v: str) -> str:
        """Ensure value is not empty.

        Parameters
        ----------
        v : str
            value to be used to identify the object.

        Returns
        -------
            str
                string value of the name field.

        Raises
        ------
            ValueError
                 if value is empty.

        """
        if not v or v.strip() == '':
            raise ValueError('value must be a non-empty string')
        return v
