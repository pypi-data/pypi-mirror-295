# openapi_client.WebsocketApi

All URIs are relative to *https://walletapi.zarban.io*

Method | HTTP request | Description
------------- | ------------- | -------------
[**ws_get**](WebsocketApi.md#ws_get) | **GET** /ws | Websocket Upgrade


# **ws_get**
> ws_get()

Websocket Upgrade

Upgrade to websocket connection

### Example

```python
from __future__ import print_function
import time
import openapi_client
from openapi_client.rest import ApiException
from pprint import pprint
# Defining the host is optional and defaults to https://walletapi.zarban.io
# See configuration.py for a list of all supported configuration parameters.
configuration = openapi_client.Configuration(
    host = "https://walletapi.zarban.io"
)


# Enter a context with an instance of the API client
with openapi_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = openapi_client.WebsocketApi(api_client)
    
    try:
        # Websocket Upgrade
        api_instance.ws_get()
    except ApiException as e:
        print("Exception when calling WebsocketApi->ws_get: %s\n" % e)
```

### Parameters
This endpoint does not need any parameter.

### Return type

void (empty response body)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: Not defined

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**101** | Switching Protocols |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

