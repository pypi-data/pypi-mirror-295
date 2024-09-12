"""Nexthink API Response Management Class."""


from typing import Union, TypeAlias
from urllib.parse import urlparse
from http import HTTPStatus
from requests.models import Response
from pydantic import BaseModel, Field, ConfigDict


from nexthink_api.Enrichment.nxt_success_response import NxtSuccessResponse
from nexthink_api.Enrichment.nxt_partial_success_response import NxtPartialSuccessResponse
from nexthink_api.Enrichment.nxt_bad_request_response import NxtBadRequestResponse
from nexthink_api.Enrichment.nxt_forbidden_response import NxtForbiddenResponse
from nexthink_api.Models.nxt_endpoint import NxtEndpoint
from nexthink_api.Models.nxt_invalid_token_request import NxtInvalidTokenRequest
from nexthink_api.Models.nxt_token_response import NxtTokenResponse
from nexthink_api.Exceptions.nxt_api_exception import NxtApiException
from nexthink_api.Nql.nxt_nql_api_execute_response import NxtNqlApiExecuteResponse
from nexthink_api.Nql.nxt_nql_api_execute_v2_response import NxtNqlApiExecuteV2Response
from nexthink_api.Nql.nxt_nql_api_export_response import NxtNqlApiExportResponse
from nexthink_api.Nql.nxt_nql_api_status_response import NxtNqlApiStatusResponse
from nexthink_api.Nql.nxt_error_response import NxtErrorResponse


__all__ = [
    'NxtResponse',
    'ResponseApiType',
    'EnrichmentResponseType',
    'ActResponseType',
    'NqlResponseType',
    'CampaignResponseType',
    'WorkflowResponseType',
]


# Enrichment response type
EnrichmentResponseType: TypeAlias = Union[
    NxtSuccessResponse,
    NxtPartialSuccessResponse,
    NxtBadRequestResponse,
    NxtInvalidTokenRequest,
    NxtForbiddenResponse
]

# Act (Remote Action) response type
ActResponseType: TypeAlias = Union[
    NxtSuccessResponse,
    # NxtErrorResponse,
    # NxtExecutionResponse
]

# Nql response type
NqlResponseType: TypeAlias = Union[
    NxtNqlApiExecuteResponse,
    NxtNqlApiExecuteV2Response,
    NxtNqlApiExportResponse,
    NxtNqlApiStatusResponse,
    NxtErrorResponse
]

# Campaign response type
CampaignResponseType: TypeAlias = Union[
    NxtSuccessResponse,
    # NxtTriggerErrorResponse,
    # NxtTriggerSuccessResponse
]

# Workflow response type
WorkflowResponseType: TypeAlias = Union[
    NxtSuccessResponse,
    # NxtExecutionResponse
]

# using an alias to make the code more readable
ResponseApiType: TypeAlias = Union[
    NxtTokenResponse,
    EnrichmentResponseType,
    ActResponseType,
    NqlResponseType,
    CampaignResponseType,
    WorkflowResponseType,
]


class NxtResponse(BaseModel):
    """Build different types of Nexthink API responses based on the provided Response object.

    Parameters
    ----------
        response : Response
            The response object to build the response from.

    Returns
    -------
        ResponseType

    Raises
    ------
        NxtApiException
            If the status code is not one of the expected values.

    """

    response: ResponseApiType = Field(alias='value', default=None)

    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True
    )

    @property
    def value(self) -> ResponseApiType:
        """Returns the value of the 'response' attribute."""
        return self.response

    def from_response(self, response: Response) -> ResponseApiType:
        """Build a Nexthink API response based on the provided Response object.

        Parameters
        ----------
            response : Response
                The response object to build the response from.

        Returns
        -------
            ResponseAPIType
                The built response.

        Raises
        ------
            NxtApiException
                If the status code is not one of the expected values.

        """
        endpoint = urlparse(response.url).path
        api = NxtEndpoint.get_api_name(endpoint)
        if api == NxtEndpoint.Enrichment.name:
            return self.build_nxt_enrichment_response(response)
        if api == NxtEndpoint.Act.name:
            return self.build_nxt_act_response(response)
        if api == NxtEndpoint.Engage.name:
            return self.build_nxt_engage_response(response)
        if api == NxtEndpoint.Workflow.name:
            return self.build_nxt_workflow_response(response)
        if api in ['Nql', 'NqlV2', 'NqlExport', 'NqlStatus']:
            return self.build_nxt_nql_response(response)
        if api == NxtEndpoint.Token.name:
            return self.build_nxt_token_response(response)
        raise NxtApiException(f"Can't create response for the API: '{api}'")

    # noinspection PyMethodMayBeStatic
    def build_nxt_enrichment_response(self, response: Response) -> EnrichmentResponseType:
        """Create Enrichment response based on the provided response object.

        Parameters
        ----------
            response : Response
                The response object to build the response from.

        Returns
        -------
            EnrichmentResponseType
                The response object based on the status code of the given response.

        Raises
        ------
            NxtApiException
                 If the status code is not one of the expected values.

        """
        status_code = response.status_code
        if status_code == HTTPStatus.OK:
            return NxtSuccessResponse()
        if status_code == HTTPStatus.MULTI_STATUS:
            data = response.json()
            return NxtPartialSuccessResponse.model_validate(data)
        if status_code == HTTPStatus.BAD_REQUEST:
            data = response.json()
            return NxtBadRequestResponse(errors=data['errors'])
        if status_code == HTTPStatus.UNAUTHORIZED:
            return NxtInvalidTokenRequest()
        if status_code == HTTPStatus.FORBIDDEN:
            return NxtForbiddenResponse(message=response.reason)
        raise NxtApiException(f"Unknown status response code: {status_code}")

    def build_nxt_act_response(self, response: Response) -> ActResponseType:
        """Create Act response based on the provided response object.

        Parameters
        ----------
            response : Response
                The response object to build the response from.

        Returns
        -------
            ActResponseType
                The response object based on the status code of the given response.

        Raises
        ------
            NxtApiException
                If the status code is not one of the expected values.

        """
        pass

    def build_nxt_workflow_response(self, response: Response) -> WorkflowResponseType:
        """Create Workflow response based on the provided response object.

        Parameters
        ----------
            response : Response
                The response object to build the response from.

        Returns
        -------
            WorkflowResponseType
                The response object based on the status code of the given response.

        Raises
        ------
            NxtApiException
                If the status code is not one of the expected values.

        """
        pass

    def build_nxt_engage_response(self, response: Response) -> CampaignResponseType:
        """Create Engage response based on the provided response object.

        Parameters
        ----------
            response : Response
                The response object to build the response from.

        Returns
        -------
            CampaignResponseType
                The response object based on the status code of the given response.

        Raises
        ------
            NxtApiException
                If the status code is not one of the expected values.

        """
        pass

    # noinspection PyMethodMayBeStatic
    def build_nxt_nql_response(self, response: Response) -> NqlResponseType:
        """Create Nql response based on the provided response object.

        Parameters
        ----------
            response : Response
                The response object to build the response from.

        Returns
        -------
            NqlResponseType
                The response object based on the status code of the given response.

        Raises
        ------
            NxtApiException
                If the status code is not one of the expected values.

        """
        status_code = response.status_code
        if status_code == HTTPStatus.OK:
            url = urlparse(response.url)
            api = NxtEndpoint.get_api_name(url.path)
            data = response.json()
            if api == NxtEndpoint.Nql.name:
                return NxtNqlApiExecuteResponse.model_validate(data)
            if api == NxtEndpoint.NqlV2.name:
                return NxtNqlApiExecuteV2Response.model_validate(data)
            if api == NxtEndpoint.NqlExport.name:
                return NxtNqlApiExportResponse.model_validate(data)
            if api == NxtEndpoint.NqlStatus.name:
                return NxtNqlApiStatusResponse.model_validate(data)
            # pylint: disable=no-member
            return NxtErrorResponse(message=f"Can't find API for {url.path}", code=HTTPStatus.IM_A_TEAPOT)
        if status_code in [
            HTTPStatus.UNAUTHORIZED,
            HTTPStatus.FORBIDDEN,
            HTTPStatus.NOT_FOUND,
            HTTPStatus.NOT_ACCEPTABLE,
            HTTPStatus.INTERNAL_SERVER_ERROR,
            HTTPStatus.SERVICE_UNAVAILABLE
        ]:
            return NxtErrorResponse(message=response.reason, code=status_code)
        raise NxtApiException(f"Unknown status response code: {status_code}")

    # noinspection PyMethodMayBeStatic
    def build_nxt_token_response(self, response: Response) -> NxtTokenResponse:
        """Create a Token response based on the provided response object.

        Parameters
        ----------
            response : Response
                The response object to build the Token response from.

        Returns
        -------
            NxtTokenResponse
                The Token response object.

        """
        return  NxtTokenResponse.model_validate(response.json())

