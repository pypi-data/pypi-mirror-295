# openapi_client.SwapApi

All URIs are relative to *https://api.zarban.io*

Method | HTTP request | Description
------------- | ------------- | -------------
[**swap_quote_post**](SwapApi.md#swap_quote_post) | **POST** /swap/quote | Get a quote for a swap


# **swap_quote_post**
> QuoteResponse swap_quote_post(quote_request)

Get a quote for a swap

Get a quote for a swap

### Example

```python
from __future__ import print_function
import time
import openapi_client
from openapi_client.rest import ApiException
from pprint import pprint
# Defining the host is optional and defaults to https://api.zarban.io
# See configuration.py for a list of all supported configuration parameters.
configuration = openapi_client.Configuration(
    host = "https://api.zarban.io"
)


# Enter a context with an instance of the API client
with openapi_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = openapi_client.SwapApi(api_client)
    quote_request = openapi_client.QuoteRequest() # QuoteRequest | 

    try:
        # Get a quote for a swap
        api_response = api_instance.swap_quote_post(quote_request)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling SwapApi->swap_quote_post: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **quote_request** | [**QuoteRequest**](QuoteRequest.md)|  | 

### Return type

[**QuoteResponse**](QuoteResponse.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Successful response |  -  |
**400** | Bad request |  -  |
**500** | Internal server error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

