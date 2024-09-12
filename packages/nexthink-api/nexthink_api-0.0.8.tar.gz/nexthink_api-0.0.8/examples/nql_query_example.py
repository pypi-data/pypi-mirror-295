# pylint: skip-file
# ruff: noqa

import os
import sys
from pprint import pprint

from nexthink_api import (
    NxtApiClient,
    NxtRegionName,
    NxtEndpoint,
    NxtNqlApiExecuteRequest,
    NxtNqlApiExecuteResponse,
    NxtNqlApiExecuteV2Response,
    NxtNqlApiExportResponse,
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

#
# Prerequisite: In Nexthink, create an API request "check_licences"
# devices | summarize NbDevices = count() by collector.tag_string
#
NX_GET_ALL_MAC = "#check_licences"
nqlRequest = NxtNqlApiExecuteRequest(queryId=NX_GET_ALL_MAC)

Endpoint = NxtEndpoint.Nql
EndpointV2 = NxtEndpoint.NqlV2
EndpointExport = NxtEndpoint.NqlExport

# Use one of previous endpoints
response = nxtClient.run_nql(Endpoint, data=nqlRequest)

if isinstance(response, NxtNqlApiExecuteResponse) or isinstance(response, NxtNqlApiExecuteV2Response):
    print("number of rows: ", end="")
    pprint(response.rows)
    print("data:")
    pprint(response.data)
    print("execution date time: ", end="")
    pprint(response.executionDateTime)
elif isinstance(response, NxtNqlApiExportResponse):
    print("Display 10 first lines of export")
    response = nxtClient.wait_status(response)
    pprint(response)
    res = nxtClient.download_export(response)
    first_lines = [line for line in res.text.split('\n')[:10]]
    for line in first_lines:
        print(line)
else:
    pprint(response)
