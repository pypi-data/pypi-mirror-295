"""Nexthink Enrichment API Module.

This module contains the classes necessary to represent and manipulate objects used in the Nexthink Enrichment API.
The classes are defined using Pydantic for data validation.

The `NxtEnrichmentRequest` class, is a transcription of the Enrichment Request object described
in the Nexthink Enrichment API.

For more information, refer to the official Nexthink Enrichment API documentation:
https://developer.nexthink.com/docs/api/enrichment-api/schemas/enrichment-request

Classes:
    - NxtEnrichmentRequest: Represents a request to enrich objects with desired fields and values.
"""

from pydantic import BaseModel, conlist, Field

from nexthink_api.Enrichment.nxt_enrichment import NxtEnrichment

__all__ = ["NxtEnrichmentRequest"]


class NxtEnrichmentRequest(BaseModel):
    """Objects to be enriched (with desired fields and values) and domain (configurable) .

    Attributes
    ----------
        enrichments : list[NxtEnrichment]
            A list of NxtEnrichment objects to be enriched.
        domain : str
            The domain for the enrichment process. For information and tracking purposes mainly

    """

    enrichments: conlist(NxtEnrichment, min_length=1, max_length=5000)
    domain: str = Field(min_length=1)
