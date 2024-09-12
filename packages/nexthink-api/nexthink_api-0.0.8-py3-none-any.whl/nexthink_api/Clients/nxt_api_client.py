"""Class used to send requests and build responses from the Nexthink Enrichment API."""

import base64
from typing import Union, Optional
from urllib.parse import urljoin
import time
from io import StringIO
from http import HTTPStatus
import pandas as pd
import requests


from nexthink_api import NxtException
from nexthink_api.Models.nxt_settings import NxtSettings
from nexthink_api.Models.nxt_endpoint import NxtEndpoint
from nexthink_api.Models.nxt_region_name import NxtRegionName
from nexthink_api.Models.nxt_token_request import NxtTokenRequest
from nexthink_api.Models.nxt_token_response import NxtTokenResponse
from nexthink_api.Exceptions.nxt_token_exception import NxtTokenException
from nexthink_api.Exceptions.nxt_status_exception import NxtStatusException
from nexthink_api.Exceptions.nxt_export_exception import NxtExportException
from nexthink_api.Exceptions.nxt_timeout_exception import NxtStatusTimeoutException
from nexthink_api.Enrichment.nxt_enrichment_request import NxtEnrichmentRequest
from nexthink_api.Nql.nxt_nql_api_execute_request import NxtNqlApiExecuteRequest
from nexthink_api.Nql.nxt_nql_api_status_response import NxtNqlApiStatusResponse
from nexthink_api.Nql.nxt_nql_api_export_response import NxtNqlApiExportResponse
from nexthink_api.Nql.nxt_error_response import NxtErrorResponse
from nexthink_api.Nql.nxt_nql_status import NxtNqlStatus
from nexthink_api.Utils.nxt_yaml_parser import NxtYamlParser
from nexthink_api.Clients.nxt_response import (
    ResponseApiType,
    NxtResponse,
    EnrichmentResponseType,
    NqlResponseType
)


__all__ = ["NxtApiClient"]


class NxtApiClient:
    """Initializes a new instance of the NxtApiClient class.

    Parameters
    ----------
        instance : str
            The name of the Nexthink instance.
        region : NxtRegionName
            The region of the Nexthink instance.
        client_id : str
            The client ID for authentication.
        client_secret : str
            The client secret for authentication.
        proxies : Optional[dict]
            A dictionary of proxies to use for the requests. Defaults to None.

    > ### Note.
    >   - if proxy are not provided, it will try to detect proxies from environment variables
    >   - if no proxy are detected, it will disable the proxy
    >   - false value disable the proxy

    """

    # pylint: disable=too-many-arguments
    def __init__(self,
                 instance: str,
                 region: NxtRegionName,
                 client_id: str,
                 client_secret: str,
                 proxies=None):  # noqa: ANN001
        """Initialize a new instance of the NxtApiClient class.

        Parameters
        ----------
            instance : str
                The name of the Nexthink instance.
            region : NxtRegionName
                The region of the Nexthink instance.
            client_id : str
                The client ID for authentication.
            client_secret : str
                The client secret for authentication.
            proxies : Optional[dict]
                A dictionary of proxies to use for the requests. Defaults to None.

            > ### Note.
            >   - if proxy are not provided, it will try to detect proxies from environment variables
            >   - if no proxy are detected, it will disable the proxy
            >   - false value disable the proxy


        """
        self.settings = NxtSettings(instance=instance, region=region, proxies=proxies)
        self.endpoint: NxtEndpoint
        self.token: Union[NxtTokenResponse, None] = None
        self.headers = {}
        self.init_token(client_id, client_secret)

    def init_token(self, client_id: str, client_secret: str) -> None:
        """Initialize the token using the provided client ID and client secret.

        Parameters
        ----------
            client_id : str
                The client ID.
            client_secret : str
                The client secret.

        Returns
        -------
            None

        """
        self.create_autorisation(client_id, client_secret)
        if self.get_bearer_token():
            self.update_header()

    def update_header(self, endpoint: NxtEndpoint = None) -> None:
        """Update header for subsequent requests based on the given endpoint.

        Parameters
        ----------
            endpoint : NxtEndpoint, optional
                The endpoint type for which to update the header. Defaults to None.

        Returns
        -------
            None

        """
        # Update header for subsequent requests
        access_token = getattr(self.token, 'access_token', None)
        if endpoint in [None, NxtEndpoint.NqlExport, NxtEndpoint.NqlStatus]:
            self.headers = {
                "Authorization": f"Bearer {access_token}",
                "Content-Type" : "application/json",
                "Accept"       : "application/json, text/csv",
            }
        else:
            self.headers = {
                "Authorization": f"Bearer {access_token}",
                "Content-Type": "application/json",
                "Accept": "application/json",
            }

    def create_autorisation(self, client_id: str, client_secret: str) -> None:
        """Create authorization using client ID and client secret.

        Parameters
        ----------
            client_id : str
                The client ID.
            client_secret :str
                The client secret.

        Returns
        -------
            None

        """
        if self.token is None:
            credentials: str = base64.b64encode(f"{client_id}:{client_secret}".encode()).decode()
            self.headers['Authorization'] = f'Basic {credentials}'

    def get_bearer_token(self) -> bool:
        """Retrieve a bearer token from the server.

        Returns
        -------
            bool
                True if the token was successfully retrieved, False otherwise.

        Raises
        ------
            NxtTokenException
                If an error occurs during the token retrieval.

        """
        try:
            return_value = False
            # Prepare to request token
            data = NxtTokenRequest().get_request_header()
            # Endpoint for token request
            url = urljoin(str(self.settings.infinity_base_uri), NxtEndpoint.Token.value)
            # Request the token
            response = requests.post(url, headers=self.headers, json=data, proxies=self.settings.proxies, timeout=300)
            if response.status_code == HTTPStatus.OK:
                nxt_response = NxtResponse()
                nxt_result = nxt_response.from_response(response=response)
                self.token = nxt_result
                return_value = True
            return return_value

        # In case of raise_for_status has generated an Exception
        except requests.exceptions.HTTPError as e:
            # Something went wrong
            raise NxtTokenException(f"Error during token retrieval: {e}") from e

    def run_enrichment(self, endpoint: NxtEndpoint, data: NxtEnrichmentRequest) -> EnrichmentResponseType:
        """Run an enrichment request on the specified endpoint using the provided data.

        Parameter
        ----
            endpoint : NxtEndpoint
                The endpoint to run the enrichment request on.
            data : NxtEnrichmentRequest
                The data containing the enrichment request.

        Raises
        ------
            ValueError
                If the specified HTTP method is not supported.

        Returns
        -------
            EnrichmentResponseType
                The EnrichmentResponseType object containing the response from the API call.

        """
        if not self.check_method(endpoint, 'POST'):
            raise ValueError('Unsupported HTTP method')
        self.update_header(endpoint)
        return self.post(endpoint, data)

    def run_nql(self,
                endpoint: NxtEndpoint,
                data: NxtNqlApiExecuteRequest,
                method: Optional[str] = None) -> NqlResponseType:
        """Run an NQL query on the specified endpoint using the provided data.

        Parameters
        ----------
            endpoint : NxtEndpoint
                The endpoint to run the NQL query on.
            data NxtNqlApiExecuteRequest
                The data containing the NQL query.
            method : Optional[str], optional
                The HTTP method to use for the request. Defaults to 'POST'.

        Raises
        ------
            ValueError
                If the specified HTTP method is not supported.

        Returns
        -------
            NqlResponseType
                The nql response object containing the response from the API call.

        """
        method = method or 'POST'
        if not self.check_method(endpoint, method):
            raise ValueError('Unsupported HTTP method')
        self.update_header(endpoint)
        if method == 'POST':
            return self.post(endpoint, data)
        return self.get(endpoint, data)

    def wait_status(
            self,
            value: NxtNqlApiExportResponse,
            timeout: int = 300
    ) -> Union[NxtNqlApiStatusResponse, NxtErrorResponse]:
        """Wait for the status of an NQL API export request to complete.

        Parameters
        ----------
            value : NxtNqlApiExportResponse
                The export request to check the status of.
            timeout : int, optional
                The maximum time to wait for the status to complete. Defaults to 300.

        Returns
        -------
            Union[NxtNqlApiStatusResponse, NxtErrorResponse]
                The final status response of the export request.

        """
        start = time.time()
        status = NxtNqlApiStatusResponse(status=NxtNqlStatus.SUBMITTED)
        while status.status in [NxtNqlStatus.SUBMITTED, NxtNqlStatus.IN_PROGRESS]:
            status = self.get_status_export(value)
            if isinstance(status, NxtErrorResponse):
                return status
            if time.time() - start > timeout:
                raise NxtStatusTimeoutException("Status not completed before timeout")
            time.sleep(1)
        return status

    def get_status_export(self, value: NxtNqlApiExportResponse) -> NqlResponseType:
        """Retrieve the status of an export based on the provided NxtNqlApiExportResponse value.

        Constructs the export status URL and makes a GET request to fetch the status.
        Converts the response to a NxtNqlStatus object and returns it.

        Parameters
        ----------
            value : NxtNqlApiExportResponse
                The export response object containing export ID.

        Returns
        -------
            NqlResponseType
                The status of the export operation.

        """
        export_status_url = urljoin(str(self.settings.infinity_base_uri), NxtEndpoint.NqlStatus.value + '/')
        export_status_url = urljoin(export_status_url, value.exportId)
        response = requests.get(export_status_url, headers=self.headers, proxies=self.settings.proxies, timeout=300)
        nxt_response = NxtResponse()
        response_status = nxt_response.from_response(response=response)
        return response_status

    def download_export(self, value: NxtNqlApiStatusResponse, timeout: int = 300) -> requests.models.Response:
        """Download an export file based on the NxtNqlApiStatusResponse value and a timeout period.

        Parameters
        ----------
            value : NxtNqlApiStatusResponse
                The status response object containing the export details.
            timeout : int, optional
                The timeout period for the download request in seconds. Defaults to 300.

        Returns
        -------
            requests.models.Response
                The response object from the download request.

        """
        if value.status != NxtNqlStatus.COMPLETED:
            raise NxtStatusException("Try do download an export not completed")
        return requests.get(value.resultsFileUrl, proxies=self.settings.proxies, timeout=timeout)

    def download_export_as_df(self, value: NxtNqlApiStatusResponse, timeout: int = 300) -> pd.DataFrame:
        """Download an export file as a pandas DataFrame based on the NxtNqlApiStatusResponse value and a timeout period.

        Parameters
        ----------
            value : NxtNqlApiStatusResponse
                The status response object containing the export details.
            timeout : int, optional
                The timeout period for the download request in seconds. Defaults to 300.

        Returns
        -------
            pd.DataFrame
                The downloaded dataframe.

        """
        response = self.download_export(value, timeout)
        if response.status_code == 200:
            return pd.read_csv(StringIO(response.text))
        else:
            raise NxtExportException(f'Failed to download export:Status code {response.status_code}')

    # noinspection PyMethodMayBeStatic
    def check_method(self, endpoint: NxtEndpoint, method: str) -> bool:
        """Check if a given method is supported for a specific endpoint.

        Parameters
        ----------
            endpoint : NxtEndpoint
                The endpoint to check the method for.
            method : str
                The method to check.

        Returns
        -------
            bool
                True if the method is supported, False otherwise.

        """
        nxt_yaml_parser = NxtYamlParser()
        api = nxt_yaml_parser.get_api_for_endpoint(endpoint)
        methods = nxt_yaml_parser.get_methods_for_api(api)
        return method in methods.get(endpoint.value, [])

    def get(self,
            endpoint: NxtEndpoint,
            params=None) -> ResponseApiType:  # noqa: ANN001
        """Send a GET request to the specified endpoint with optional query parameters.

        Parameters
        ----------
            endpoint : NxtEndpoint
                The endpoint to send the request to.
            params : Optional[Dict[str, Any]]
                Query parameters to include in the request. Defaults to None.

        Returns
        -------
            ResponseAPIType
                The response object containing the status of the request.

        Raises
        ------
            requests.exceptions.RequestException
                If there was an error sending the request.

        """
        url = urljoin(str(self.settings.infinity_base_uri), endpoint.value)
        response = requests.get(url, headers=self.headers, params=params, proxies=self.settings.proxies, timeout=300)
        nxt_response = NxtResponse()
        response_status = nxt_response.from_response(response=response)
        return response_status

    def post(self,
             endpoint: NxtEndpoint,
             data: Union[NxtTokenRequest, NxtEnrichmentRequest, NxtNqlApiExecuteRequest]) -> ResponseApiType:
        """Send a POST request to the specified endpoint with the provided data.

        Parameters
        ----------
            endpoint : (NxtEndpoint
                The endpoint to send the request to.
            data : Union[NxtTokenRequest, NxtEnrichmentRequest, NxtNqlApiExecuteRequest])
                The data to be sent in the request.

        Returns
        -------
             ResponseAPIType
                The response object containing the status of the POST request.

        """
        url = urljoin(str(self.settings.infinity_base_uri), endpoint.value)
        response = requests.post(url,
                                 headers=self.headers,
                                 json=data.model_dump(),
                                 proxies=self.settings.proxies,
                                 timeout=300)
        nxt_response = NxtResponse()
        response_status = nxt_response.from_response(response=response)
        return response_status
