# openapi_client.AccountsApi

All URIs are relative to *https://api.zarban.io*

Method | HTTP request | Description
------------- | ------------- | -------------
[**accounts_address_get**](AccountsApi.md#accounts_address_get) | **GET** /accounts/{address} | Get account by address


# **accounts_address_get**
> Account accounts_address_get(address)

Get account by address

Get account by address

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
    api_instance = openapi_client.AccountsApi(api_client)
    address = '0x1234567890123456789012345678901234567890' # str | Ethereum address of the account

    try:
        # Get account by address
        api_response = api_instance.accounts_address_get(address)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling AccountsApi->accounts_address_get: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **address** | **str**| Ethereum address of the account | 

### Return type

[**Account**](Account.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Account details |  -  |
**400** | Bad request |  -  |
**404** | Not found |  -  |
**500** | Internal server error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

