"""NQL Status response state."""

from enum import Enum

__all__ = ["NxtNqlStatus"]


class NxtNqlStatus(str, Enum):
    """NQL Status response state."""

    SUBMITTED = "SUBMITTED"
    IN_PROGRESS = "IN_PROGRESS"
    ERROR = "ERROR"
    COMPLETED = "COMPLETED"
