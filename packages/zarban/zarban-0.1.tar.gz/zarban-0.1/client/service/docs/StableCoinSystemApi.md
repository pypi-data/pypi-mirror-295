# openapi_client.StableCoinSystemApi

All URIs are relative to *https://api.zarban.io*

Method | HTTP request | Description
------------- | ------------- | -------------
[**ilks_get**](StableCoinSystemApi.md#ilks_get) | **GET** /ilks | Get all Ilks
[**ilks_name_get**](StableCoinSystemApi.md#ilks_name_get) | **GET** /ilks/{name} | Get Ilk by name
[**permissions_matrix_get**](StableCoinSystemApi.md#permissions_matrix_get) | **GET** /permissions/matrix | Get authorization matrix
[**proxies_get**](StableCoinSystemApi.md#proxies_get) | **GET** /proxies | Retrieves proxies owned by a specific owner
[**stablecoinsystem_tx_createvault_post**](StableCoinSystemApi.md#stablecoinsystem_tx_createvault_post) | **POST** /stablecoinsystem/tx/createvault | Create vault
[**stablecoinsystem_tx_depositcollateral_post**](StableCoinSystemApi.md#stablecoinsystem_tx_depositcollateral_post) | **POST** /stablecoinsystem/tx/depositcollateral | Deposit collateral
[**stablecoinsystem_tx_mintzar_post**](StableCoinSystemApi.md#stablecoinsystem_tx_mintzar_post) | **POST** /stablecoinsystem/tx/mintzar | Mint ZAR
[**stablecoinsystem_tx_repayzar_post**](StableCoinSystemApi.md#stablecoinsystem_tx_repayzar_post) | **POST** /stablecoinsystem/tx/repayzar | Repay ZAR
[**stablecoinsystem_tx_withdrawcollateral_post**](StableCoinSystemApi.md#stablecoinsystem_tx_withdrawcollateral_post) | **POST** /stablecoinsystem/tx/withdrawcollateral | Withdraw collateral
[**stats_get**](StableCoinSystemApi.md#stats_get) | **GET** /stats | Get collector data
[**vaults_get**](StableCoinSystemApi.md#vaults_get) | **GET** /vaults | Get vaults by owner query
[**vaults_id_events_get**](StableCoinSystemApi.md#vaults_id_events_get) | **GET** /vaults/{id}/events | Get vault events by ID
[**vaults_id_get**](StableCoinSystemApi.md#vaults_id_get) | **GET** /vaults/{id} | Get a vault by ID


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
    api_instance = openapi_client.StableCoinSystemApi(api_client)
    
    try:
        # Get all Ilks
        api_response = api_instance.ilks_get()
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling StableCoinSystemApi->ilks_get: %s\n" % e)
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
    api_instance = openapi_client.StableCoinSystemApi(api_client)
    name = 'name_example' # str | Name of the ILK

    try:
        # Get Ilk by name
        api_response = api_instance.ilks_name_get(name)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling StableCoinSystemApi->ilks_name_get: %s\n" % e)
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
    api_instance = openapi_client.StableCoinSystemApi(api_client)
    
    try:
        # Get authorization matrix
        api_response = api_instance.permissions_matrix_get()
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling StableCoinSystemApi->permissions_matrix_get: %s\n" % e)
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

# **proxies_get**
> list[Proxy] proxies_get(owner)

Retrieves proxies owned by a specific owner

Returns a list of proxies filtered by the owner's address.

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
    api_instance = openapi_client.StableCoinSystemApi(api_client)
    owner = 'owner_example' # str | The Ethereum address of the owner.

    try:
        # Retrieves proxies owned by a specific owner
        api_response = api_instance.proxies_get(owner)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling StableCoinSystemApi->proxies_get: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **owner** | **str**| The Ethereum address of the owner. | 

### Return type

[**list[Proxy]**](Proxy.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | A JSON array of proxies |  -  |
**400** | Bad request |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **stablecoinsystem_tx_createvault_post**
> list[ChainActivity] stablecoinsystem_tx_createvault_post(stablecoin_system_create_vault_tx_request)

Create vault

Create vault

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
    api_instance = openapi_client.StableCoinSystemApi(api_client)
    stablecoin_system_create_vault_tx_request = openapi_client.StablecoinSystemCreateVaultTxRequest() # StablecoinSystemCreateVaultTxRequest | Create vault transaction request

    try:
        # Create vault
        api_response = api_instance.stablecoinsystem_tx_createvault_post(stablecoin_system_create_vault_tx_request)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling StableCoinSystemApi->stablecoinsystem_tx_createvault_post: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **stablecoin_system_create_vault_tx_request** | [**StablecoinSystemCreateVaultTxRequest**](StablecoinSystemCreateVaultTxRequest.md)| Create vault transaction request | 

### Return type

[**list[ChainActivity]**](ChainActivity.md)

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

# **stablecoinsystem_tx_depositcollateral_post**
> list[ChainActivity] stablecoinsystem_tx_depositcollateral_post(stablecoin_system_deposit_collateral_tx_request)

Deposit collateral

Deposit collateral

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
    api_instance = openapi_client.StableCoinSystemApi(api_client)
    stablecoin_system_deposit_collateral_tx_request = openapi_client.StablecoinSystemDepositCollateralTxRequest() # StablecoinSystemDepositCollateralTxRequest | Deposit collateral transaction request

    try:
        # Deposit collateral
        api_response = api_instance.stablecoinsystem_tx_depositcollateral_post(stablecoin_system_deposit_collateral_tx_request)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling StableCoinSystemApi->stablecoinsystem_tx_depositcollateral_post: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **stablecoin_system_deposit_collateral_tx_request** | [**StablecoinSystemDepositCollateralTxRequest**](StablecoinSystemDepositCollateralTxRequest.md)| Deposit collateral transaction request | 

### Return type

[**list[ChainActivity]**](ChainActivity.md)

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

# **stablecoinsystem_tx_mintzar_post**
> list[ChainActivity] stablecoinsystem_tx_mintzar_post(stablecoin_system_mint_zar_tx_request)

Mint ZAR

Mint ZAR

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
    api_instance = openapi_client.StableCoinSystemApi(api_client)
    stablecoin_system_mint_zar_tx_request = openapi_client.StablecoinSystemMintZarTxRequest() # StablecoinSystemMintZarTxRequest | Mint ZAR transaction request

    try:
        # Mint ZAR
        api_response = api_instance.stablecoinsystem_tx_mintzar_post(stablecoin_system_mint_zar_tx_request)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling StableCoinSystemApi->stablecoinsystem_tx_mintzar_post: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **stablecoin_system_mint_zar_tx_request** | [**StablecoinSystemMintZarTxRequest**](StablecoinSystemMintZarTxRequest.md)| Mint ZAR transaction request | 

### Return type

[**list[ChainActivity]**](ChainActivity.md)

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

# **stablecoinsystem_tx_repayzar_post**
> list[ChainActivity] stablecoinsystem_tx_repayzar_post(stablecoin_system_repay_zar_tx_request)

Repay ZAR

Repay ZAR

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
    api_instance = openapi_client.StableCoinSystemApi(api_client)
    stablecoin_system_repay_zar_tx_request = openapi_client.StablecoinSystemRepayZarTxRequest() # StablecoinSystemRepayZarTxRequest | Repay ZAR transaction request

    try:
        # Repay ZAR
        api_response = api_instance.stablecoinsystem_tx_repayzar_post(stablecoin_system_repay_zar_tx_request)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling StableCoinSystemApi->stablecoinsystem_tx_repayzar_post: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **stablecoin_system_repay_zar_tx_request** | [**StablecoinSystemRepayZarTxRequest**](StablecoinSystemRepayZarTxRequest.md)| Repay ZAR transaction request | 

### Return type

[**list[ChainActivity]**](ChainActivity.md)

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

# **stablecoinsystem_tx_withdrawcollateral_post**
> list[ChainActivity] stablecoinsystem_tx_withdrawcollateral_post(stablecoin_system_withdraw_collateral_tx_request)

Withdraw collateral

Withdraw collateral

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
    api_instance = openapi_client.StableCoinSystemApi(api_client)
    stablecoin_system_withdraw_collateral_tx_request = openapi_client.StablecoinSystemWithdrawCollateralTxRequest() # StablecoinSystemWithdrawCollateralTxRequest | Withdraw collateral transaction request

    try:
        # Withdraw collateral
        api_response = api_instance.stablecoinsystem_tx_withdrawcollateral_post(stablecoin_system_withdraw_collateral_tx_request)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling StableCoinSystemApi->stablecoinsystem_tx_withdrawcollateral_post: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **stablecoin_system_withdraw_collateral_tx_request** | [**StablecoinSystemWithdrawCollateralTxRequest**](StablecoinSystemWithdrawCollateralTxRequest.md)| Withdraw collateral transaction request | 

### Return type

[**list[ChainActivity]**](ChainActivity.md)

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
    api_instance = openapi_client.StableCoinSystemApi(api_client)
    
    try:
        # Get collector data
        api_response = api_instance.stats_get()
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling StableCoinSystemApi->stats_get: %s\n" % e)
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
    api_instance = openapi_client.StableCoinSystemApi(api_client)
    owner = 'owner_example' # str | Ethereum address of the owner (optional)

    try:
        # Get vaults by owner query
        api_response = api_instance.vaults_get(owner=owner)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling StableCoinSystemApi->vaults_get: %s\n" % e)
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
    api_instance = openapi_client.StableCoinSystemApi(api_client)
    id = 56 # int | Vault ID
type = 'type_example' # str | Event type (optional)

    try:
        # Get vault events by ID
        api_response = api_instance.vaults_id_events_get(id, type=type)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling StableCoinSystemApi->vaults_id_events_get: %s\n" % e)
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
    api_instance = openapi_client.StableCoinSystemApi(api_client)
    id = 56 # int | Vault ID

    try:
        # Get a vault by ID
        api_response = api_instance.vaults_id_get(id)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling StableCoinSystemApi->vaults_id_get: %s\n" % e)
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

