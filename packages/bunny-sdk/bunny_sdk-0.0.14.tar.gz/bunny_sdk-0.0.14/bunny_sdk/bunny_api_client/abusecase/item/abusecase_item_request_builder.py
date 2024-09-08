from __future__ import annotations
from dataclasses import dataclass, field
from kiota_abstractions.base_request_builder import BaseRequestBuilder
from kiota_abstractions.base_request_configuration import RequestConfiguration
from kiota_abstractions.default_query_parameters import QueryParameters
from kiota_abstractions.get_path_parameters import get_path_parameters
from kiota_abstractions.method import Method
from kiota_abstractions.request_adapter import RequestAdapter
from kiota_abstractions.request_information import RequestInformation
from kiota_abstractions.request_option import RequestOption
from kiota_abstractions.serialization import Parsable, ParsableFactory
from typing import Any, Callable, Dict, List, Optional, TYPE_CHECKING, Union
from warnings import warn

if TYPE_CHECKING:
    from ...models.abuse_cases.abuse_case import AbuseCase
    from .check.check_request_builder import CheckRequestBuilder
    from .resolve.resolve_request_builder import ResolveRequestBuilder

class AbusecaseItemRequestBuilder(BaseRequestBuilder):
    """
    Builds and executes requests for operations under /abusecase/{id}
    """
    def __init__(self,request_adapter: RequestAdapter, path_parameters: Union[str, Dict[str, Any]]) -> None:
        """
        Instantiates a new AbusecaseItemRequestBuilder and sets the default values.
        param path_parameters: The raw url or the url-template parameters for the request.
        param request_adapter: The request adapter to use to execute the requests.
        Returns: None
        """
        super().__init__(request_adapter, "{+baseurl}/abusecase/{id}", path_parameters)
    
    async def get(self,request_configuration: Optional[RequestConfiguration[QueryParameters]] = None) -> Optional[AbuseCase]:
        """
        [GetAbuseCase API Docs](https://docs.bunny.net/reference/abusecasepublic_getabusecase2)
        param request_configuration: Configuration for the request such as headers, query parameters, and middleware options.
        Returns: Optional[AbuseCase]
        """
        request_info = self.to_get_request_information(
            request_configuration
        )
        if not self.request_adapter:
            raise Exception("Http core is null") 
        from ...models.abuse_cases.abuse_case import AbuseCase

        return await self.request_adapter.send_async(request_info, AbuseCase, None)
    
    def to_get_request_information(self,request_configuration: Optional[RequestConfiguration[QueryParameters]] = None) -> RequestInformation:
        """
        [GetAbuseCase API Docs](https://docs.bunny.net/reference/abusecasepublic_getabusecase2)
        param request_configuration: Configuration for the request such as headers, query parameters, and middleware options.
        Returns: RequestInformation
        """
        request_info = RequestInformation(Method.GET, self.url_template, self.path_parameters)
        request_info.configure(request_configuration)
        request_info.headers.try_add("Accept", "application/json")
        return request_info
    
    def with_url(self,raw_url: str) -> AbusecaseItemRequestBuilder:
        """
        Returns a request builder with the provided arbitrary URL. Using this method means any other path or query parameters are ignored.
        param raw_url: The raw URL to use for the request builder.
        Returns: AbusecaseItemRequestBuilder
        """
        if raw_url is None:
            raise TypeError("raw_url cannot be null.")
        return AbusecaseItemRequestBuilder(self.request_adapter, raw_url)
    
    @property
    def check(self) -> CheckRequestBuilder:
        """
        The check property
        """
        from .check.check_request_builder import CheckRequestBuilder

        return CheckRequestBuilder(self.request_adapter, self.path_parameters)
    
    @property
    def resolve(self) -> ResolveRequestBuilder:
        """
        The resolve property
        """
        from .resolve.resolve_request_builder import ResolveRequestBuilder

        return ResolveRequestBuilder(self.request_adapter, self.path_parameters)
    
    @dataclass
    class AbusecaseItemRequestBuilderGetRequestConfiguration(RequestConfiguration[QueryParameters]):
        """
        Configuration for the request such as headers, query parameters, and middleware options.
        """
        warn("This class is deprecated. Please use the generic RequestConfiguration class generated by the generator.", DeprecationWarning)
    

