"""Enrichment information for the given object, composed of the name of field to be enriched and the desired value."""

from typing import Union
from typing_extensions import Self
from pydantic import BaseModel, Field, field_serializer, model_validator, InstanceOf

from nexthink_api.Enrichment.nxt_field_name import NxtFieldName

__all__ = ["NxtField"]


# TODO: add date string format support for the value property
# Will use the enum value with serialize
class NxtField(BaseModel):
    """Enrichment information for the given object, composed of the name of field to be enriched and the desired value.

    Ensures constraints on the 'name' attribute based on the presence of '#' character.
    Raises ValueError if constraints are violated.
    Converts 'name' attribute to a string when converting to a dictionary.
    """

    name: InstanceOf[NxtFieldName]
    value: Union[str, int]
    custom_value: str = Field(default=None, exclude=True, repr=False)

    # Add constraints to name
    # If name doesn't contain #, then customValue must be None
    # If name contains #, then customValue must be specified
    @model_validator(mode='after')
    def check_name(self) -> Self:
        """Validate the 'name' attribute of the model after it has been instantiated.

        if value contains '#', then customValue must be specified.
        if value doesn't contain '#', then customValue must not be None.

        Raises
        ------
            ValueError
                If condition on 'customValue' is violated.

        Returns
        -------
            Self: The instance of the model.

        """
        if '#' in self.name.value and self.custom_value is None:
            raise ValueError("You cannot use a FieldName of type Custom without specifying a customValue.")
        if '#' not in self.name.value and self.custom_value is not None:
            raise ValueError("You cannot use a customValue without specifying a FieldName of type Custom.")
        return self

    @field_serializer('name')
    def name(self, value: NxtFieldName) -> str:
        """Return the value of the 'name' attribute when converting to a dictionary.

        Parameters
        ----------
        value : NxtFieldName
            Enum from which we must get the name

        Returns
        -------
            str
                The value of the 'name' attribute.
        -------

        """
        return self.get_field_name(value)

    def get_field_name(self, name: NxtFieldName) -> str:
        """Format the Enrichment field name with custom value if required.

        Parameters
        ----------
        name : NxtFieldName
            Field to Enrich.

        Returns
        -------
            str
                The Enrich field value, followed by # and custom value for custom Field.

        """
        max_custom_field_length = 64
        if self.custom_value is not None and '#' in name.value:
            updated_value = name.value.format(self.custom_value)
            if len(updated_value) > max_custom_field_length:
                raise ValueError(f"Resulting string exceeds 64 characters: {updated_value}")
            return updated_value
        if '#' in name.value:
            raise ValueError(f"Missing 'customValue' parameter for custom field: {name}")

        return name.value
