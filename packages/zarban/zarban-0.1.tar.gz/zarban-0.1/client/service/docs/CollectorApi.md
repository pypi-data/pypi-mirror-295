# openapi_client.CollectorApi

All URIs are relative to *https://api.zarban.io*

Method | HTTP request | Description
------------- | ------------- | -------------
[**stats_get**](CollectorApi.md#stats_get) | **GET** /stats | Get collector data


# **stats_get**
> Stats stats_get()

Get collector data

Get collector data

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
    api_instance = openapi_client.CollectorApi(api_client)
    
    try:
        # Get collector data
        api_response = api_instance.stats_get()
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling CollectorApi->stats_get: %s\n" % e)
```

### Parameters
This endpoint does not need any parameter.

### Return type

[**Stats**](Stats.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | A JSON object with collector data |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

