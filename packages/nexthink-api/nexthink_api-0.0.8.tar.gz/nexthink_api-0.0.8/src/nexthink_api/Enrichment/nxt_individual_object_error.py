"""Error for an individual object, composed of identification information about the object and the list of errors."""

from pydantic import BaseModel, conlist, Field, ConfigDict

from nexthink_api.Enrichment.nxt_identification import NxtIdentification
from nexthink_api.Enrichment.nxt_identification_name import NxtIdentificationName
from nexthink_api.Enrichment.nxt_error import NxtError

__all__ = ["NxtIndividualObjectError"]


class NxtIndividualObjectError(BaseModel):
    """Error for an individual object, composed of identification information about the object and the list of errors.

    Attributes
    ----------
        identification : [NxtIdentification]
            List containing a single NxtIdentification instance.
        errors : list[NxtError]
            List containing NxtError instances.
        model_config : ConfigDict
            Configuration dictionary allowing arbitrary types.

    """

    identification: conlist(NxtIdentification, min_length=1, max_length=1) = Field(
            default_factory=lambda: [NxtIdentification(name=NxtIdentificationName(value='default_name'),
                                                       value='default_value')])
    errors: conlist(NxtError, min_length=1) = Field(
            default_factory=lambda: [NxtError(message='default_message',
                                              code='default_value')])
    model_config = ConfigDict(arbitrary_types_allowed=True, )
