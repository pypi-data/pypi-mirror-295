# openapi_client.AddressesApi

All URIs are relative to *https://api.zarban.io*

Method | HTTP request | Description
------------- | ------------- | -------------
[**addresses_get**](AddressesApi.md#addresses_get) | **GET** /addresses | Get all addresses


# **addresses_get**
> list[Address] addresses_get(format=format)

Get all addresses

All addresses knows to Zarban.

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
    api_instance = openapi_client.AddressesApi(api_client)
    format = 'format_example' # str | The type of addresses to return (optional)

    try:
        # Get all addresses
        api_response = api_instance.addresses_get(format=format)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling AddressesApi->addresses_get: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **format** | **str**| The type of addresses to return | [optional] 

### Return type

[**list[Address]**](Address.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | A JSON object with addresses |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

