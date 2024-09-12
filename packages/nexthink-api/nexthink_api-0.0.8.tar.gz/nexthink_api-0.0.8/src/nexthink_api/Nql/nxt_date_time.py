"""Datetime class object for NQL answer."""

from datetime import datetime
from typing import Self
from typing_extensions import Annotated
from pydantic import BaseModel, Field, field_validator, model_validator

__all__ = ["NxtDateTime"]


class NxtDateTime(BaseModel):
    """Datetime class object for NQL answer.

    Attributes
    ----------
        year : int
            year (2 or 4 digits).
        month : int
            month (1-12).
        day : int
            day (1-31).
        hour : int
            hour (0-23).
        minute : int
            minute (0-59).
        second : int
            second (0-59).

    Raises
    ------
        ValueError
            when year is not 2-digits or 4-digit number.

    """

    year: Annotated[int, Field(strict=True)]
    month: Annotated[int, Field(strict=True, ge=1, le=12)]
    day: Annotated[int, Field(strict=True, ge=1, le=31)]
    hour: Annotated[int, Field(strict=True, ge=0, le=23)]
    minute: Annotated[int, Field(strict=True, ge=0, le=59)]
    second: Annotated[int, Field(strict=True, ge=0, le=59)]

    # noinspection PyNestedDecorators
    @field_validator('year', mode='before')
    @classmethod
    def validate_year(cls, value: int) -> int:
        """Ensure year is 2-digit or 4-digit.

        Parameters
        ----------
            value : int
                year to validate.

        Returns
        -------
            int
                valid year.

        Raises
        ------
            ValueError
                when year is not 2-digits or 4-digit number.

        """
        if value <= 99:  # noqa: PLR2004
            value += 2000  # noqa: PLR2004
        elif value > 9999:  # noqa: PLR2004
            raise ValueError("Year must be either 2 digits or 4 digit number)")
        return value

    @model_validator(mode='after')
    def validate_date(self) -> Self:
        """Verify is a date can be created with these parameters."""
        try:
            datetime(self.year, self.month, self.day, self.hour, self.minute, self.second)
        except ValueError as e:
            raise ValueError(f'date parameters are not valid: {e}') from e
        return self
