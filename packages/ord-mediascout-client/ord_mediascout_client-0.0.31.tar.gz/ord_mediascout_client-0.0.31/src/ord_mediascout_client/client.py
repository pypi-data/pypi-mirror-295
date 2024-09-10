import logging
from typing import Any, Optional, Type

import requests
from pydantic.error_wrappers import ValidationError
from pydantic.main import BaseModel
from pydantic.tools import parse_raw_as
from requests.auth import HTTPBasicAuth

from .config import ORDMediascoutConfig
from .feed_models import (
    CreateContainerWebApiDto,
    CreateFeedElementsBulkWebApiDto,
    CreateFeedElementsWebApiDto,
    EditFeedElementWebApiDto,
    GetContainerWebApiDto,
    GetFeedElementsBulkInfo,
    GetFeedElementsWebApiDto,
    ResponseContainerWebApiDto,
    ResponseCreateFeedElementsBulkWebApiDto,
    ResponseEditFeedElementWebApiDto,
    ResponseFeedElementsWebApiDto,
    ResponseGetContainerWebApiDto,
    ResponseGetFeedElementsBulkInfo,
    ResponseGetFeedElementsWebApiDto,
)
from .models import (
    BadRequestResponse,
    ClearInvoiceDataWebApiDto,
    ClientResponse,
    CreateClientRequest,
    CreateCreativeRequest,
    CreatedCreativeResponse,
    CreateFinalContractRequest,
    CreateInitialContractRequest,
    CreateInvoicelessStatisticsRequest,
    CreateInvoiceRequest,
    CreateOuterContractRequest,
    CreatePlatformRequest,
    CreativeGroupResponse,
    CreativeResponse,
    EditCreativeRequest,
    EditFinalContractWebApiDto,
    EditInitialContractWebApiDto,
    EditInvoiceDataWebApiDto,
    EditInvoiceStatisticsWebApiDto,
    EditOuterContractWebApiDto,
    EditPlatformWebApiDto,
    EntityIdResponse,
    FinalContractResponse,
    GetClientRequest,
    GetCreativeGroupsRequest,
    GetCreativesWebApiDto,
    GetFinalContractsRequest,
    GetInitialContractRequest,
    GetInvoicelessPeriodsRequest,
    GetInvoicesWebApiDto,
    GetOuterContractsRequest,
    InitialContractResponse,
    InvoicelessStatisticsResponse,
    InvoiceResponse,
    InvoiceSummaryResponse,
    OuterContractResponse,
    PlatformResponse,
    SupplementInvoiceWebApiDto,
)


class APIError(Exception):
    pass


class ResponseError(APIError):
    def __init__(self, response: requests.Response):
        super().__init__(
            f'Response error {response.status_code} for API {response.request.method} {response.request.url}'
        )
        self.response = response


class BadResponseError(APIError):
    def __init__(self, response: requests.Response, error: Optional[BadRequestResponse] = None):
        super().__init__(error and error.errorType or f'Bad response from API: {response.status_code}')
        self.response = response
        self.error = error


class TemporaryResponseError(APIError):
    def __init__(self, response: requests.Response):
        super().__init__(f'Temporary error: {response.status_code}')
        self.response = response


class UnexpectedResponseError(APIError):
    def __init__(self, response: requests.Response):
        super().__init__(f'Unexpected response with STATUS_CODE: {response.status_code}')
        self.response = response


class APIValidationError(APIError):
    def __init__(self, e: ValidationError):
        if callable(e.errors):
            error_list = e.errors()
            if error_list:
                error_message = error_list[0]
                loc = error_message.get('loc', [])
                msg = error_message.get('msg', 'Unknown message')
                error_details = f"ValidationError: '{loc[-1] if loc else 'Unknown field'} {msg}'"
            else:
                error_details = 'ValidationError: No error details available'
        else:
            error_details = 'ValidationError: Unable to retrieve error details'
        super().__init__(error_details)


class ORDMediascoutClient:
    def __init__(self, config: ORDMediascoutConfig):
        self.config = config
        self.auth = HTTPBasicAuth(self.config.username, self.config.password)
        self.headers = {'Content-Type': 'application/json-patch+json'}
        self.logger = logging.getLogger('ord_mediascout_client')

    def _call(
        self,
        method: str,
        url: str,
        obj: Optional[BaseModel] = None,
        return_type: Optional[Type[Any]] = None,
        **kwargs: dict[str, Any],
    ) -> Any:
        try:
            response = requests.request(
                method,
                f'{self.config.url}{url}',
                data=obj and obj.json(),
                auth=self.auth,
                headers=self.headers,
                **kwargs,
            )
            self.logger.debug(
                f'API call: {method} {url}\n'
                f'Headers: {self.headers}\n'
                f'Body: {obj and obj.json(indent=4)}\n'
                f'Response: {response.status_code}\n'
                f'{response.text}'
            )
        except requests.RequestException as e:
            self.logger.exception(
                f'API call: {method} {url}\n'
                f'Headers: {self.headers}\n'
                f'Body: {obj and obj.json(indent=4)}\n'
                f'Exception: {e}\n'
            )
            raise APIError from e

        match response.status_code:
            case 400 | 401:
                try:
                    bad_response = BadRequestResponse.parse_raw(response.text)
                except ValidationError as e:
                    raise UnexpectedResponseError(response) from e
                raise BadResponseError(response, bad_response)
            case int() if 500 <= response.status_code < 600:
                raise TemporaryResponseError(response)
            case 200 | 201:
                if return_type is not None:
                    try:
                        return parse_raw_as(return_type, response.text or '{}')
                    except ValidationError as e:
                        raise APIValidationError(e) from e
            case _:
                raise UnexpectedResponseError(response)

    # Clients
    def create_client(self, client: CreateClientRequest) -> ClientResponse:
        client: ClientResponse = self._call(
            'post', f'{self.config.api_url_prefix}/clients/createclient', client, ClientResponse
        )
        return client

    def get_clients(self, parameters: GetClientRequest) -> list[ClientResponse]:
        clients: list[ClientResponse] = self._call(
            'post', f'{self.config.api_url_prefix}/clients/getclients', parameters, list[ClientResponse]
        )
        return clients

    # Contracts
    def create_initial_contract(self, contract: CreateInitialContractRequest) -> InitialContractResponse:
        contract: InitialContractResponse = self._call(
            'post', f'{self.config.api_url_prefix}/contracts/createinitialcontract', contract, InitialContractResponse
        )
        return contract

    def edit_initial_contract(self, contract: EditInitialContractWebApiDto) -> InitialContractResponse:
        contract: InitialContractResponse = self._call(
            'post', f'{self.config.api_url_prefix}/contracts/editinitialcontract', contract, InitialContractResponse
        )
        return contract

    def get_initial_contracts(self, parameters: GetInitialContractRequest) -> list[InitialContractResponse]:
        contracts: list[InitialContractResponse] = self._call(
            'post',
            f'{self.config.api_url_prefix}/contracts/getinitialcontracts',
            parameters,
            list[InitialContractResponse],
        )
        return contracts

    def create_final_contract(self, contract: CreateFinalContractRequest) -> FinalContractResponse:
        contract: FinalContractResponse = self._call(
            'post', f'{self.config.api_url_prefix}/contracts/createfinalcontract', contract, FinalContractResponse
        )
        return contract

    def edit_final_contract(self, contract: EditFinalContractWebApiDto) -> FinalContractResponse:
        contract: FinalContractResponse = self._call(
            'post', f'{self.config.api_url_prefix}/contracts/editfinalcontract', contract, FinalContractResponse
        )
        return contract

    def get_final_contracts(self, parameters: GetFinalContractsRequest) -> list[FinalContractResponse]:
        contracts: list[FinalContractResponse] = self._call(
            'post', f'{self.config.api_url_prefix}/contracts/getfinalcontracts', parameters, list[FinalContractResponse]
        )
        return contracts

    def create_outer_contract(self, contract: CreateOuterContractRequest) -> OuterContractResponse:
        contract: OuterContractResponse = self._call(
            'post', f'{self.config.api_url_prefix}/contracts/createoutercontract', contract, OuterContractResponse
        )
        return contract

    def edit_outer_contract(self, contract: EditOuterContractWebApiDto) -> OuterContractResponse:
        contract: OuterContractResponse = self._call(
            'post', f'{self.config.api_url_prefix}/contracts/editoutercontract', contract, OuterContractResponse
        )
        return contract

    def get_outer_contracts(self, parameters: GetOuterContractsRequest) -> list[OuterContractResponse]:
        contracts: list[OuterContractResponse] = self._call(
            'post', f'{self.config.api_url_prefix}/contracts/getoutercontracts', parameters, list[OuterContractResponse]
        )
        return contracts

    # Creatives
    def create_creative(self, creative: CreateCreativeRequest) -> CreatedCreativeResponse:
        creative: CreatedCreativeResponse = self._call(
            'post', f'{self.config.api_url_prefix}/creatives/createcreative', creative, CreatedCreativeResponse
        )
        return creative

    def edit_creative(self, creative: EditCreativeRequest) -> CreativeResponse:
        updated_creative: CreativeResponse = self._call(
            'post', f'{self.config.api_url_prefix}/creatives/editcreative', creative, CreativeResponse
        )
        return updated_creative

    def get_creatives(self, parameters: GetCreativesWebApiDto) -> list[CreativeResponse]:
        creatives: list[CreativeResponse] = self._call(
            'post', f'{self.config.api_url_prefix}/creatives/getcreatives', parameters, list[CreativeResponse]
        )
        return creatives

    # Creative Group
    def edit_creative_group(self, creative_group: CreativeGroupResponse) -> CreativeGroupResponse:
        updated_creative_group: CreativeGroupResponse = self._call(
            'post', f'{self.config.api_url_prefix}/creatives/editcreativegroup', creative_group, CreativeGroupResponse
        )
        return updated_creative_group

    def get_creative_groups(self, parameters: GetCreativeGroupsRequest) -> list[CreativeGroupResponse]:
        creative_groups: list[CreativeGroupResponse] = self._call(
            'post', f'{self.config.api_url_prefix}/creatives/getcreativegroups', parameters, list[CreativeGroupResponse]
        )
        return creative_groups

    # Feeds
    def create_container(self, container: CreateContainerWebApiDto) -> ResponseContainerWebApiDto:
        container: ResponseContainerWebApiDto = self._call(
            'post', '/webapi/creatives/createcontainer', container, ResponseContainerWebApiDto
        )
        return container

    def get_containers(self, parameters: GetContainerWebApiDto) -> list[ResponseGetContainerWebApiDto]:
        containers: list[ResponseGetContainerWebApiDto] = self._call(
            'post', '/webapi/creatives/getcontainers', parameters, list[ResponseGetContainerWebApiDto]
        )
        return containers

    def create_feed_elements(self, feed_elements: CreateFeedElementsWebApiDto) -> list[ResponseFeedElementsWebApiDto]:
        feed_elements: list[ResponseFeedElementsWebApiDto] = self._call(
            'post', '/webapi/creatives/createfeedelements', feed_elements, list[ResponseFeedElementsWebApiDto]
        )
        return feed_elements

    def edit_feed_element(self, feed_element: EditFeedElementWebApiDto) -> ResponseEditFeedElementWebApiDto:
        feed_element: ResponseEditFeedElementWebApiDto = self._call(
            'post', '/webapi/creatives/editfeedelement', feed_element, ResponseEditFeedElementWebApiDto
        )
        return feed_element

    def get_feed_elements(self, parameters: GetFeedElementsWebApiDto) -> list[ResponseGetFeedElementsWebApiDto]:
        feed_elements: list[ResponseGetFeedElementsWebApiDto] = self._call(
            'post', '/webapi/creatives/getfeedelements', parameters, list[ResponseGetFeedElementsWebApiDto]
        )
        return feed_elements

    def create_feed_elements_bulk(
        self, feed_elements_bulk: CreateFeedElementsBulkWebApiDto
    ) -> ResponseCreateFeedElementsBulkWebApiDto:
        feed_elements_bulk: ResponseCreateFeedElementsBulkWebApiDto = self._call(
            'post',
            '/webapi/creatives/createfeedelementsbulk',
            feed_elements_bulk,
            ResponseCreateFeedElementsBulkWebApiDto,
        )
        return feed_elements_bulk

    def get_feed_elements_bulk_info(
        self, feed_elements_bulk_info: GetFeedElementsBulkInfo
    ) -> ResponseGetFeedElementsBulkInfo:
        feed_elements_bulk_info: ResponseGetFeedElementsBulkInfo = self._call(
            'post',
            '/webapi/creatives/getfeedelementsbulkinfo',
            feed_elements_bulk_info,
            ResponseGetFeedElementsBulkInfo,
        )
        return feed_elements_bulk_info

    # Invoices
    def create_invoice(self, invoice: CreateInvoiceRequest) -> EntityIdResponse:
        entity: EntityIdResponse = self._call(
            'post', f'{self.config.api_url_prefix}/invoices/createinvoice', invoice, EntityIdResponse
        )
        return entity

    def edit_invoice(self, invoice: EditInvoiceDataWebApiDto) -> InvoiceResponse:
        invoice: InvoiceResponse = self._call(
            'post', f'{self.config.api_url_prefix}/invoices/editinvoice', invoice, InvoiceResponse
        )
        return invoice

    def overwrite_invoice(self, invoice: EditInvoiceStatisticsWebApiDto) -> None:
        self._call('post', f'{self.config.api_url_prefix}/invoices/overwriteinvoice', invoice)

    def clear_invoice(self, invoice: ClearInvoiceDataWebApiDto) -> None:
        self._call('post', f'{self.config.api_url_prefix}/invoices/clearinvoice', invoice)

    def supplement_invoice(self, invoice: SupplementInvoiceWebApiDto) -> EntityIdResponse:
        entity: EntityIdResponse = self._call(
            'post', f'{self.config.api_url_prefix}/invoices/supplementinvoice', invoice, EntityIdResponse
        )
        return entity

    def get_invoices(self, parameters: GetInvoicesWebApiDto) -> list[InvoiceResponse]:
        invoices: list[InvoiceResponse] = self._call(
            'post', f'{self.config.api_url_prefix}/invoices/getinvoices', parameters, list[InvoiceResponse]
        )
        return invoices

    def get_invoice_summary(self, entity: EntityIdResponse) -> InvoiceSummaryResponse:
        invoice_summary: InvoiceSummaryResponse = self._call(
            'post', f'{self.config.api_url_prefix}/invoices/getinvoicesummary', entity, InvoiceSummaryResponse
        )
        return invoice_summary

    def confirm_invoice(self, entity: EntityIdResponse) -> None:
        self._call('post', f'{self.config.api_url_prefix}/invoices/confirminvoice', entity)

    def delete_invoice(self, entity: EntityIdResponse) -> None:
        self._call('post', f'{self.config.api_url_prefix}/invoices/deleteinvoices', entity)

    # WebApiPlatform
    def create_platform(self, platform: CreatePlatformRequest) -> EntityIdResponse:
        entity: EntityIdResponse = self._call(
            'post', f'{self.config.api_url_prefix}/platforms/createplatform', platform, EntityIdResponse
        )
        return entity

    def edit_platform(self, platform: EditPlatformWebApiDto) -> PlatformResponse:
        updated_platform: PlatformResponse = self._call(
            'post', f'{self.config.api_url_prefix}/platforms/editplatform', platform, PlatformResponse
        )
        return updated_platform

    # Statistics
    def create_statistics(self, statistics: CreateInvoicelessStatisticsRequest) -> None:
        statistics: None = self._call(
            'post', f'{self.config.api_url_prefix}/statistics/createstatistics', statistics, None
        )
        return statistics

    def get_statistics(self, parameters: GetInvoicelessPeriodsRequest) -> list[InvoicelessStatisticsResponse]:
        statistics: list[InvoicelessStatisticsResponse] = self._call(
            'post',
            f'{self.config.api_url_prefix}/statistics/getstatistics',
            parameters,
            list[InvoicelessStatisticsResponse],
        )
        return statistics

    # PING
    def ping(self) -> bool:
        tmp_auth, self.auth = self.auth, None
        self._call('get', '/webapi/ping')
        self.auth = tmp_auth
        return True

    def ping_auth(self) -> bool:
        self._call('get', '/webapi/pingauth')
        return True
