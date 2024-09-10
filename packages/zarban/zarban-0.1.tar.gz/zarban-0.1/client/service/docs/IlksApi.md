# openapi_client.IlksApi

All URIs are relative to *https://api.zarban.io*

Method | HTTP request | Description
------------- | ------------- | -------------
[**ilks_get**](IlksApi.md#ilks_get) | **GET** /ilks | Get all Ilks
[**ilks_name_get**](IlksApi.md#ilks_name_get) | **GET** /ilks/{name} | Get Ilk by name


# **ilks_get**
> list[Ilk] ilks_get()

Get all Ilks

Retrieve a list of all available ilks.

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
    api_instance = openapi_client.IlksApi(api_client)
    
    try:
        # Get all Ilks
        api_response = api_instance.ilks_get()
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling IlksApi->ilks_get: %s\n" % e)
```

### Parameters
This endpoint does not need any parameter.

### Return type

[**list[Ilk]**](Ilk.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Successfully retrieved list of ilks |  -  |
**500** | Internal server error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **ilks_name_get**
> Ilk ilks_name_get(name)

Get Ilk by name

Retrieve an Ilk by providing its name.

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
    api_instance = openapi_client.IlksApi(api_client)
    name = 'name_example' # str | Name of the ILK

    try:
        # Get Ilk by name
        api_response = api_instance.ilks_name_get(name)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling IlksApi->ilks_name_get: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **name** | **str**| Name of the ILK | 

### Return type

[**Ilk**](Ilk.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Successfully retrieved ILK |  -  |
**500** | Internal server error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

