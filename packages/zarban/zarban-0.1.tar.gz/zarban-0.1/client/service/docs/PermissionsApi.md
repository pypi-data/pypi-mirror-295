# openapi_client.PermissionsApi

All URIs are relative to *https://api.zarban.io*

Method | HTTP request | Description
------------- | ------------- | -------------
[**permissions_matrix_get**](PermissionsApi.md#permissions_matrix_get) | **GET** /permissions/matrix | Get authorization matrix


# **permissions_matrix_get**
> AuthMatrix permissions_matrix_get()

Get authorization matrix

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
    api_instance = openapi_client.PermissionsApi(api_client)
    
    try:
        # Get authorization matrix
        api_response = api_instance.permissions_matrix_get()
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling PermissionsApi->permissions_matrix_get: %s\n" % e)
```

### Parameters
This endpoint does not need any parameter.

### Return type

[**AuthMatrix**](AuthMatrix.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Successful operation |  -  |
**500** | Internal Server Error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

