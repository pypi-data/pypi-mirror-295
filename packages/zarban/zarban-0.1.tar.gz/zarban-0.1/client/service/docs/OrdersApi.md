# openapi_client.OrdersApi

All URIs are relative to *https://api.zarban.io*

Method | HTTP request | Description
------------- | ------------- | -------------
[**orders_get**](OrdersApi.md#orders_get) | **GET** /orders | Fetch Unfilled Orders
[**orders_sync_post**](OrdersApi.md#orders_sync_post) | **POST** /orders/sync | Updates Order Entity


# **orders_get**
> list[Order] orders_get(type=type, hash=hash, status=status, offerer=offerer, filler=filler, decay_start_time=decay_start_time, decay_end_time=decay_end_time, deadline=deadline, cursor=cursor, limit=limit)

Fetch Unfilled Orders

Get a list of unfilled orders filtered by different parameters.

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
    api_instance = openapi_client.OrdersApi(api_client)
    type = 'type_example' # str | Type of the order (optional)
hash = 'hash_example' # str | order hash (optional)
status = 'status_example' # str | Status of the order (optional)
offerer = 'offerer_example' # str | Ethereum address of the offerer (optional)
filler = 'filler_example' # str | Ethereum address of the filler (optional)
decay_start_time = openapi_client.TimeRange() # TimeRange | Decay start time (optional)
decay_end_time = openapi_client.TimeRange() # TimeRange | Decay end time (optional)
deadline = openapi_client.TimeRange() # TimeRange | Order deadline (optional)
cursor = 56 # int | Cursor for pagination (optional)
limit = 10 # int | Limit the number of orders returned (default is 10) (optional) (default to 10)

    try:
        # Fetch Unfilled Orders
        api_response = api_instance.orders_get(type=type, hash=hash, status=status, offerer=offerer, filler=filler, decay_start_time=decay_start_time, decay_end_time=decay_end_time, deadline=deadline, cursor=cursor, limit=limit)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling OrdersApi->orders_get: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **type** | **str**| Type of the order | [optional] 
 **hash** | **str**| order hash | [optional] 
 **status** | **str**| Status of the order | [optional] 
 **offerer** | **str**| Ethereum address of the offerer | [optional] 
 **filler** | **str**| Ethereum address of the filler | [optional] 
 **decay_start_time** | [**TimeRange**](.md)| Decay start time | [optional] 
 **decay_end_time** | [**TimeRange**](.md)| Decay end time | [optional] 
 **deadline** | [**TimeRange**](.md)| Order deadline | [optional] 
 **cursor** | **int**| Cursor for pagination | [optional] 
 **limit** | **int**| Limit the number of orders returned (default is 10) | [optional] [default to 10]

### Return type

[**list[Order]**](Order.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Successful response. |  -  |
**400** | Bad request (e.g. invalid filter parameters). |  -  |
**500** | Internal Server Error. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **orders_sync_post**
> Error orders_sync_post(update_order_request)

Updates Order Entity

updates an order entity in database

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
    api_instance = openapi_client.OrdersApi(api_client)
    update_order_request = openapi_client.UpdateOrderRequest() # UpdateOrderRequest | 

    try:
        # Updates Order Entity
        api_response = api_instance.orders_sync_post(update_order_request)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling OrdersApi->orders_sync_post: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **update_order_request** | [**UpdateOrderRequest**](UpdateOrderRequest.md)|  | 

### Return type

[**Error**](Error.md)

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

