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
    from ....models.dns_zone.dns_zone import DnsZone
    from ....models.structured_bad_request_response import StructuredBadRequestResponse

class DismissnameservercheckRequestBuilder(BaseRequestBuilder):
    """
    Builds and executes requests for operations under /dnszone/{-id}/dismissnameservercheck
    """
    def __init__(self,request_adapter: RequestAdapter, path_parameters: Union[str, Dict[str, Any]]) -> None:
        """
        Instantiates a new DismissnameservercheckRequestBuilder and sets the default values.
        param path_parameters: The raw url or the url-template parameters for the request.
        param request_adapter: The request adapter to use to execute the requests.
        Returns: None
        """
        super().__init__(request_adapter, "{+baseurl}/dnszone/{%2Did}/dismissnameservercheck", path_parameters)
    
    async def post(self,request_configuration: Optional[RequestConfiguration[QueryParameters]] = None) -> Optional[DnsZone]:
        """
        [DismissDnsConfigurationNotice API Docs](https://docs.bunny.net/reference/dnszonepublic_dismissnameservercheck)
        param request_configuration: Configuration for the request such as headers, query parameters, and middleware options.
        Returns: Optional[DnsZone]
        """
        request_info = self.to_post_request_information(
            request_configuration
        )
        from ....models.structured_bad_request_response import StructuredBadRequestResponse

        error_mapping: Dict[str, ParsableFactory] = {
            "400": StructuredBadRequestResponse,
        }
        if not self.request_adapter:
            raise Exception("Http core is null") 
        from ....models.dns_zone.dns_zone import DnsZone

        return await self.request_adapter.send_async(request_info, DnsZone, error_mapping)
    
    def to_post_request_information(self,request_configuration: Optional[RequestConfiguration[QueryParameters]] = None) -> RequestInformation:
        """
        [DismissDnsConfigurationNotice API Docs](https://docs.bunny.net/reference/dnszonepublic_dismissnameservercheck)
        param request_configuration: Configuration for the request such as headers, query parameters, and middleware options.
        Returns: RequestInformation
        """
        request_info = RequestInformation(Method.POST, self.url_template, self.path_parameters)
        request_info.configure(request_configuration)
        request_info.headers.try_add("Accept", "application/json")
        return request_info
    
    def with_url(self,raw_url: str) -> DismissnameservercheckRequestBuilder:
        """
        Returns a request builder with the provided arbitrary URL. Using this method means any other path or query parameters are ignored.
        param raw_url: The raw URL to use for the request builder.
        Returns: DismissnameservercheckRequestBuilder
        """
        if raw_url is None:
            raise TypeError("raw_url cannot be null.")
        return DismissnameservercheckRequestBuilder(self.request_adapter, raw_url)
    
    @dataclass
    class DismissnameservercheckRequestBuilderPostRequestConfiguration(RequestConfiguration[QueryParameters]):
        """
        Configuration for the request such as headers, query parameters, and middleware options.
        """
        warn("This class is deprecated. Please use the generic RequestConfiguration class generated by the generator.", DeprecationWarning)
    

