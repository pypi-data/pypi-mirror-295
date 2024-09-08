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
    from .abusecase_get_response import AbusecaseGetResponse
    from .item.abusecase_item_request_builder import AbusecaseItemRequestBuilder

class AbusecaseRequestBuilder(BaseRequestBuilder):
    """
    Builds and executes requests for operations under /abusecase
    """
    def __init__(self,request_adapter: RequestAdapter, path_parameters: Union[str, Dict[str, Any]]) -> None:
        """
        Instantiates a new AbusecaseRequestBuilder and sets the default values.
        param path_parameters: The raw url or the url-template parameters for the request.
        param request_adapter: The request adapter to use to execute the requests.
        Returns: None
        """
        super().__init__(request_adapter, "{+baseurl}/abusecase?page={page}&perPage={perPage}", path_parameters)
    
    def by_id(self,id: int) -> AbusecaseItemRequestBuilder:
        """
        Gets an item from the BunnyApiClient.abusecase.item collection
        param id: Unique identifier of the item
        Returns: AbusecaseItemRequestBuilder
        """
        if id is None:
            raise TypeError("id cannot be null.")
        from .item.abusecase_item_request_builder import AbusecaseItemRequestBuilder

        url_tpl_params = get_path_parameters(self.path_parameters)
        url_tpl_params["id"] = id
        return AbusecaseItemRequestBuilder(self.request_adapter, url_tpl_params)
    
    async def get(self,request_configuration: Optional[RequestConfiguration[AbusecaseRequestBuilderGetQueryParameters]] = None) -> Optional[AbusecaseGetResponse]:
        """
        [ListAbuseCases API Docs](https://docs.bunny.net/reference/abusecasepublic_index)
        param request_configuration: Configuration for the request such as headers, query parameters, and middleware options.
        Returns: Optional[AbusecaseGetResponse]
        """
        request_info = self.to_get_request_information(
            request_configuration
        )
        if not self.request_adapter:
            raise Exception("Http core is null") 
        from .abusecase_get_response import AbusecaseGetResponse

        return await self.request_adapter.send_async(request_info, AbusecaseGetResponse, None)
    
    def to_get_request_information(self,request_configuration: Optional[RequestConfiguration[AbusecaseRequestBuilderGetQueryParameters]] = None) -> RequestInformation:
        """
        [ListAbuseCases API Docs](https://docs.bunny.net/reference/abusecasepublic_index)
        param request_configuration: Configuration for the request such as headers, query parameters, and middleware options.
        Returns: RequestInformation
        """
        request_info = RequestInformation(Method.GET, self.url_template, self.path_parameters)
        request_info.configure(request_configuration)
        request_info.headers.try_add("Accept", "application/json")
        return request_info
    
    def with_url(self,raw_url: str) -> AbusecaseRequestBuilder:
        """
        Returns a request builder with the provided arbitrary URL. Using this method means any other path or query parameters are ignored.
        param raw_url: The raw URL to use for the request builder.
        Returns: AbusecaseRequestBuilder
        """
        if raw_url is None:
            raise TypeError("raw_url cannot be null.")
        return AbusecaseRequestBuilder(self.request_adapter, raw_url)
    
    @dataclass
    class AbusecaseRequestBuilderGetQueryParameters():
        """
        [ListAbuseCases API Docs](https://docs.bunny.net/reference/abusecasepublic_index)
        """
        def get_query_parameter(self,original_name: str) -> str:
            """
            Maps the query parameters names to their encoded names for the URI template parsing.
            param original_name: The original query parameter name in the class.
            Returns: str
            """
            if original_name is None:
                raise TypeError("original_name cannot be null.")
            if original_name == "per_page":
                return "perPage"
            if original_name == "page":
                return "page"
            return original_name
        
        page: Optional[int] = None

        per_page: Optional[int] = None

    
    @dataclass
    class AbusecaseRequestBuilderGetRequestConfiguration(RequestConfiguration[AbusecaseRequestBuilderGetQueryParameters]):
        """
        Configuration for the request such as headers, query parameters, and middleware options.
        """
        warn("This class is deprecated. Please use the generic RequestConfiguration class generated by the generator.", DeprecationWarning)
    

