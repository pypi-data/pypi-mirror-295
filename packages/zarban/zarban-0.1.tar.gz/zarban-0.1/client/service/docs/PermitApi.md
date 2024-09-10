# openapi_client.PermitApi

All URIs are relative to *https://api.zarban.io*

Method | HTTP request | Description
------------- | ------------- | -------------
[**permit_single_get**](PermitApi.md#permit_single_get) | **GET** /permit/single | Get permit for single token


# **permit_single_get**
> PermitSingle permit_single_get(token, user)

Get permit for single token

Get permit for single token

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
    api_instance = openapi_client.PermitApi(api_client)
    token = 'token_example' # str | Ethereum address of the token
user = 'user_example' # str | Ethereum address of the user

    try:
        # Get permit for single token
        api_response = api_instance.permit_single_get(token, user)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling PermitApi->permit_single_get: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **token** | **str**| Ethereum address of the token | 
 **user** | **str**| Ethereum address of the user | 

### Return type

[**PermitSingle**](PermitSingle.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Successful response |  -  |
**400** | Bad request |  -  |
**500** | Internal server error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

