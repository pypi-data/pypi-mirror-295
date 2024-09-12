"""Classes necessary to send requests and build responses from the Nexthink Enrichment API."""

from nexthink_api.Clients.nxt_response import (
    NxtResponse,
    ResponseApiType,
    EnrichmentResponseType,
    ActResponseType,
    NqlResponseType,
    CampaignResponseType,
    WorkflowResponseType,
)
from nexthink_api.Clients.nxt_api_client import NxtApiClient

__all__ = [
    'NxtApiClient',
    'NxtResponse',
    'ResponseApiType',
    'EnrichmentResponseType',
    'ActResponseType',
    'NqlResponseType',
    'CampaignResponseType',
    'WorkflowResponseType',
]
