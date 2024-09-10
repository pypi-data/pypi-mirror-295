# openapi_client.BorrowsApi

All URIs are relative to *https://api.zarban.io*

Method | HTTP request | Description
------------- | ------------- | -------------
[**lendingpool_borrows_get**](BorrowsApi.md#lendingpool_borrows_get) | **GET** /lendingpool/borrows | Get user borrows of lendingpool


# **lendingpool_borrows_get**
> list[LendingpoolBorrow] lendingpool_borrows_get(user=user, reserve=reserve, cursor=cursor, limit=limit)

Get user borrows of lendingpool

Get user borrows of lendingpool

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
    api_instance = openapi_client.BorrowsApi(api_client)
    user = 'user_example' # str | Ethereum address of the user (optional)
reserve = 'reserve_example' # str | Ethereum address of the reserve (optional)
cursor = 56 # int | Cursor for pagination (optional)
limit = 50 # int | Limit the number of deposits returned (default is 50) (optional) (default to 50)

    try:
        # Get user borrows of lendingpool
        api_response = api_instance.lendingpool_borrows_get(user=user, reserve=reserve, cursor=cursor, limit=limit)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling BorrowsApi->lendingpool_borrows_get: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **user** | **str**| Ethereum address of the user | [optional] 
 **reserve** | **str**| Ethereum address of the reserve | [optional] 
 **cursor** | **int**| Cursor for pagination | [optional] 
 **limit** | **int**| Limit the number of deposits returned (default is 50) | [optional] [default to 50]

### Return type

[**list[LendingpoolBorrow]**](LendingpoolBorrow.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | List of user borrows |  -  |
**400** | Bad request |  -  |
**500** | Internal server error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

