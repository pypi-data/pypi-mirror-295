# openapi_client.VaultsApi

All URIs are relative to *https://api.zarban.io*

Method | HTTP request | Description
------------- | ------------- | -------------
[**vaults_get**](VaultsApi.md#vaults_get) | **GET** /vaults | Get vaults by owner query
[**vaults_id_events_get**](VaultsApi.md#vaults_id_events_get) | **GET** /vaults/{id}/events | Get vault events by ID
[**vaults_id_get**](VaultsApi.md#vaults_id_get) | **GET** /vaults/{id} | Get a vault by ID


# **vaults_get**
> list[Vault] vaults_get(owner=owner)

Get vaults by owner query

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
    api_instance = openapi_client.VaultsApi(api_client)
    owner = 'owner_example' # str | Ethereum address of the owner (optional)

    try:
        # Get vaults by owner query
        api_response = api_instance.vaults_get(owner=owner)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling VaultsApi->vaults_get: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **owner** | **str**| Ethereum address of the owner | [optional] 

### Return type

[**list[Vault]**](Vault.md)

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
**404** | Not found |  -  |
**500** | Internal server error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **vaults_id_events_get**
> list[BasicEvent] vaults_id_events_get(id, type=type)

Get vault events by ID

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
    api_instance = openapi_client.VaultsApi(api_client)
    id = 56 # int | Vault ID
type = 'type_example' # str | Event type (optional)

    try:
        # Get vault events by ID
        api_response = api_instance.vaults_id_events_get(id, type=type)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling VaultsApi->vaults_id_events_get: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **int**| Vault ID | 
 **type** | **str**| Event type | [optional] 

### Return type

[**list[BasicEvent]**](BasicEvent.md)

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
**404** | Not found |  -  |
**500** | Internal server error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **vaults_id_get**
> Vault vaults_id_get(id)

Get a vault by ID

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
    api_instance = openapi_client.VaultsApi(api_client)
    id = 56 # int | Vault ID

    try:
        # Get a vault by ID
        api_response = api_instance.vaults_id_get(id)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling VaultsApi->vaults_id_get: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **int**| Vault ID | 

### Return type

[**Vault**](Vault.md)

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
**404** | Not found |  -  |
**500** | Internal server error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

