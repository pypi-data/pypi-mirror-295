"""Class for fields to be enriched and values to be assigned."""

from pydantic import BaseModel, conlist

from nexthink_api.Enrichment.nxt_identification import NxtIdentification
from nexthink_api.Enrichment.nxt_field import NxtField


__all__ = ["NxtEnrichment"]


class NxtEnrichment(BaseModel):
    """Enrichment class.

    Enrichment composed of the identification information of the desired object
    and the fields to be enriched (names and values).

    Attributes
    ----------
            identification : List[NxtIdentification])
                List containing one NxtIdentification object for identification purposes.
            fields : List[NxtField]
                List of NxtField objects to be enriched.

    """

    identification: conlist(NxtIdentification, min_length=1, max_length=1)
    fields: conlist(NxtField, min_length=1)
