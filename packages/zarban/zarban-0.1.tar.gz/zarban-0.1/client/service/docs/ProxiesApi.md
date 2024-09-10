# openapi_client.ProxiesApi

All URIs are relative to *https://api.zarban.io*

Method | HTTP request | Description
------------- | ------------- | -------------
[**proxies_get**](ProxiesApi.md#proxies_get) | **GET** /proxies | Retrieves proxies owned by a specific owner


# **proxies_get**
> list[Proxy] proxies_get(owner)

Retrieves proxies owned by a specific owner

Returns a list of proxies filtered by the owner's address.

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
    api_instance = openapi_client.ProxiesApi(api_client)
    owner = 'owner_example' # str | The Ethereum address of the owner.

    try:
        # Retrieves proxies owned by a specific owner
        api_response = api_instance.proxies_get(owner)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling ProxiesApi->proxies_get: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **owner** | **str**| The Ethereum address of the owner. | 

### Return type

[**list[Proxy]**](Proxy.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | A JSON array of proxies |  -  |
**400** | Bad request |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

