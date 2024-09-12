"""List of regions for Nexthink servers."""

from enum import Enum


class NxtRegionName(str, Enum):
    """List of regions for Nexthink servers."""

    us = "us"       # United States
    eu = "eu"       # European Union
    pac = "pac"     # Asia Pacific
    meta = "meta"   # Middle East, Turkey, Africa
