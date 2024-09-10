# openapi_client.PricesApi

All URIs are relative to *https://api.zarban.io*

Method | HTTP request | Description
------------- | ------------- | -------------
[**prices_get**](PricesApi.md#prices_get) | **GET** /prices | List prices based on query parameters
[**prices_symbol_history_get**](PricesApi.md#prices_symbol_history_get) | **GET** /prices/{symbol}/history | Get price history for a symbol


# **prices_get**
> list[Price] prices_get(symbol=symbol)

List prices based on query parameters

Retrieve a list of price details based on specified query parameters

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
    api_instance = openapi_client.PricesApi(api_client)
    symbol = 'symbol_example' # str | Symbol of the price (optional)

    try:
        # List prices based on query parameters
        api_response = api_instance.prices_get(symbol=symbol)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling PricesApi->prices_get: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **symbol** | **str**| Symbol of the price | [optional] 

### Return type

[**list[Price]**](Price.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Successful response |  -  |
**400** | Bad Request |  -  |
**500** | Internal Server Error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **prices_symbol_history_get**
> list[Price] prices_symbol_history_get(symbol, _from=_from, to=to)

Get price history for a symbol

Get price history for a symbol

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
    api_instance = openapi_client.PricesApi(api_client)
    symbol = 'symbol_example' # str | Symbol of the price
_from = '2013-10-20T19:20:30+01:00' # datetime | Start date (optional)
to = '2013-10-20T19:20:30+01:00' # datetime | End date (optional)

    try:
        # Get price history for a symbol
        api_response = api_instance.prices_symbol_history_get(symbol, _from=_from, to=to)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling PricesApi->prices_symbol_history_get: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **symbol** | **str**| Symbol of the price | 
 **_from** | **datetime**| Start date | [optional] 
 **to** | **datetime**| End date | [optional] 

### Return type

[**list[Price]**](Price.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | List of price history |  -  |
**400** | Bad request |  -  |
**500** | Internal server error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

