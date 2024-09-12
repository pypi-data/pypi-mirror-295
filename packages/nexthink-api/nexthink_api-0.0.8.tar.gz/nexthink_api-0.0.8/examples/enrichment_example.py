# pylint: skip-file
# ruff: noqa

import os
import sys
from pprint import pprint
from datetime import datetime

from nexthink_api import (
    NxtApiClient,
    NxtRegionName,
    NxtIdentification,
    NxtIdentificationName,
    NxtField,
    NxtFieldName,
    NxtEnrichment,
    NxtEndpoint,
    NxtEnrichmentRequest,
)


client_id = os.getenv('client_id')
client_secret = os.getenv('client_secret')

https = os.getenv('https_proxy')
http = os.getenv('http_proxy')

if client_id is None or client_secret is None:
    print("client_id or client_secret not found")
    sys.exit(1)
if https is None or http is None:
    print("https or http not found")
    sys.exit(1)

nxtClient = NxtApiClient('lfdj', NxtRegionName.eu, client_id=client_id, client_secret=client_secret,)
if nxtClient.token is None:
    print("Can't get token")
    sys.exit(1)


# Creating the Enrichment record
identification = NxtIdentification(name=NxtIdentificationName.DEVICE_DEVICE_NAME, value="M71879")
field1 = NxtField(name=NxtFieldName.CUSTOM_DEVICE, value=str(datetime.now()), custom_value="clw1")
field2 = NxtField(name=NxtFieldName.CUSTOM_DEVICE, value=str(datetime.now()), custom_value="clw2")
field3 = NxtField(name=NxtFieldName.CUSTOM_DEVICE, value=str(datetime.now()), custom_value="clw3")

enrichments = [NxtEnrichment(identification=[identification], fields=[field1, field2, field3])]
enrichmentRequest = NxtEnrichmentRequest(enrichments=enrichments, domain="test_fdj")
payload = enrichmentRequest.model_dump()
pprint(payload)

# use the client to run perform the enrichment on the Enrichment endpoint
response = nxtClient.run_enrichment(endpoint=NxtEndpoint.Enrichment, data=enrichmentRequest)
pprint(response)
