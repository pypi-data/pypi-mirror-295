# openapi_client.EventsApi

All URIs are relative to *https://api.zarban.io*

Method | HTTP request | Description
------------- | ------------- | -------------
[**events_get**](EventsApi.md#events_get) | **GET** /events | Ordered list events based on query parameters


# **events_get**
> list[ExtendedEvent] events_get(domain, type, name, id=id, cursor=cursor, limit=limit, order=order)

Ordered list events based on query parameters

Retrieve a list of events based on specified query parameters

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
    api_instance = openapi_client.EventsApi(api_client)
    domain = openapi_client.EventDomain() # EventDomain | 
type = openapi_client.EventType() # EventType | Type of the event
name = openapi_client.EventName() # EventName | 
id = 56 # int | ID of the event (optional)
cursor = 56 # int | Cursor for pagination (optional)
limit = 56 # int | Maximum number of records to retrieve. Defaults to 50 if not provided. (optional)
order = 'desc' # str | Order of the events. Default is desc. (optional)

    try:
        # Ordered list events based on query parameters
        api_response = api_instance.events_get(domain, type, name, id=id, cursor=cursor, limit=limit, order=order)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling EventsApi->events_get: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **domain** | [**EventDomain**](.md)|  | 
 **type** | [**EventType**](.md)| Type of the event | 
 **name** | [**EventName**](.md)|  | 
 **id** | **int**| ID of the event | [optional] 
 **cursor** | **int**| Cursor for pagination | [optional] 
 **limit** | **int**| Maximum number of records to retrieve. Defaults to 50 if not provided. | [optional] 
 **order** | **str**| Order of the events. Default is desc. | [optional] 

### Return type

[**list[ExtendedEvent]**](ExtendedEvent.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Successful response |  -  |
**400** | Bad Request |  -  |
**500** | Internal Server Error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

