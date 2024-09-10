# openapi_client.LendingPoolApi

All URIs are relative to *https://api.zarban.io*

Method | HTTP request | Description
------------- | ------------- | -------------
[**lendingpool_borrows_get**](LendingPoolApi.md#lendingpool_borrows_get) | **GET** /lendingpool/borrows | Get user borrows of lendingpool
[**lendingpool_deposits_get**](LendingPoolApi.md#lendingpool_deposits_get) | **GET** /lendingpool/deposits | Get user deposits of Lendingpool
[**lendingpool_overview_get**](LendingPoolApi.md#lendingpool_overview_get) | **GET** /lendingpool/overview | Get lending pool overview
[**lendingpool_reserves_get**](LendingPoolApi.md#lendingpool_reserves_get) | **GET** /lendingpool/reserves | Fetch Reserve Data By Asset
[**lendingpool_tx_borrow_post**](LendingPoolApi.md#lendingpool_tx_borrow_post) | **POST** /lendingpool/tx/borrow | Borrow from lending pool
[**lendingpool_tx_deposit_post**](LendingPoolApi.md#lendingpool_tx_deposit_post) | **POST** /lendingpool/tx/deposit | Deposit to lending pool
[**lendingpool_tx_repay_post**](LendingPoolApi.md#lendingpool_tx_repay_post) | **POST** /lendingpool/tx/repay | Repay to lending pool
[**lendingpool_tx_useassetascollateral_post**](LendingPoolApi.md#lendingpool_tx_useassetascollateral_post) | **POST** /lendingpool/tx/useassetascollateral | Enable/Disable asset as collateral
[**lendingpool_tx_withdraw_post**](LendingPoolApi.md#lendingpool_tx_withdraw_post) | **POST** /lendingpool/tx/withdraw | Withdraw from lending pool


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
    api_instance = openapi_client.LendingPoolApi(api_client)
    user = 'user_example' # str | Ethereum address of the user (optional)
reserve = 'reserve_example' # str | Ethereum address of the reserve (optional)
cursor = 56 # int | Cursor for pagination (optional)
limit = 50 # int | Limit the number of deposits returned (default is 50) (optional) (default to 50)

    try:
        # Get user borrows of lendingpool
        api_response = api_instance.lendingpool_borrows_get(user=user, reserve=reserve, cursor=cursor, limit=limit)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling LendingPoolApi->lendingpool_borrows_get: %s\n" % e)
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

# **lendingpool_deposits_get**
> list[LendingpoolDeposit] lendingpool_deposits_get(user=user, reserve=reserve, cursor=cursor, limit=limit)

Get user deposits of Lendingpool

Get user deposits of Lendingpool

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
    api_instance = openapi_client.LendingPoolApi(api_client)
    user = 'user_example' # str | Ethereum address of the user (optional)
reserve = 'reserve_example' # str | Ethereum address of the reserve (optional)
cursor = 56 # int | Cursor for pagination (optional)
limit = 50 # int | Limit the number of deposits returned (default is 50) (optional) (default to 50)

    try:
        # Get user deposits of Lendingpool
        api_response = api_instance.lendingpool_deposits_get(user=user, reserve=reserve, cursor=cursor, limit=limit)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling LendingPoolApi->lendingpool_deposits_get: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **user** | **str**| Ethereum address of the user | [optional] 
 **reserve** | **str**| Ethereum address of the reserve | [optional] 
 **cursor** | **int**| Cursor for pagination | [optional] 
 **limit** | **int**| Limit the number of deposits returned (default is 50) | [optional] [default to 50]

### Return type

[**list[LendingpoolDeposit]**](LendingpoolDeposit.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | List of user deposits |  -  |
**400** | Bad request |  -  |
**500** | Internal server error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **lendingpool_overview_get**
> object lendingpool_overview_get()

Get lending pool overview

Get lending pool overview

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
    api_instance = openapi_client.LendingPoolApi(api_client)
    
    try:
        # Get lending pool overview
        api_response = api_instance.lendingpool_overview_get()
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling LendingPoolApi->lendingpool_overview_get: %s\n" % e)
```

### Parameters
This endpoint does not need any parameter.

### Return type

**object**

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | A JSON object with lending pool overview |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **lendingpool_reserves_get**
> FormattedReserveData lendingpool_reserves_get(asset=asset)

Fetch Reserve Data By Asset

Retrieve data of reserves

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
    api_instance = openapi_client.LendingPoolApi(api_client)
    asset = 'asset_example' # str | The asset address in hexadecimal format. (optional)

    try:
        # Fetch Reserve Data By Asset
        api_response = api_instance.lendingpool_reserves_get(asset=asset)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling LendingPoolApi->lendingpool_reserves_get: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **asset** | **str**| The asset address in hexadecimal format. | [optional] 

### Return type

[**FormattedReserveData**](FormattedReserveData.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Successful response. |  -  |
**400** | Bad request (e.g. invalid asset address). |  -  |
**500** | Internal Server Error. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **lendingpool_tx_borrow_post**
> InlineResponse200 lendingpool_tx_borrow_post(lendingpool_borrow_tx_request)

Borrow from lending pool

Borrow from lending pool

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
    api_instance = openapi_client.LendingPoolApi(api_client)
    lendingpool_borrow_tx_request = openapi_client.LendingpoolBorrowTxRequest() # LendingpoolBorrowTxRequest | Borrow transaction request, if amount is not provided, it will be calculated based on the token balance

    try:
        # Borrow from lending pool
        api_response = api_instance.lendingpool_tx_borrow_post(lendingpool_borrow_tx_request)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling LendingPoolApi->lendingpool_tx_borrow_post: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **lendingpool_borrow_tx_request** | [**LendingpoolBorrowTxRequest**](LendingpoolBorrowTxRequest.md)| Borrow transaction request, if amount is not provided, it will be calculated based on the token balance | 

### Return type

[**InlineResponse200**](InlineResponse200.md)

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

# **lendingpool_tx_deposit_post**
> InlineResponse200 lendingpool_tx_deposit_post(lendingpool_deposit_tx_request)

Deposit to lending pool

Deposit to lending pool

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
    api_instance = openapi_client.LendingPoolApi(api_client)
    lendingpool_deposit_tx_request = openapi_client.LendingpoolDepositTxRequest() # LendingpoolDepositTxRequest | Deposit transaction request, if amount is not provided, it will be calculated based on the token balance

    try:
        # Deposit to lending pool
        api_response = api_instance.lendingpool_tx_deposit_post(lendingpool_deposit_tx_request)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling LendingPoolApi->lendingpool_tx_deposit_post: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **lendingpool_deposit_tx_request** | [**LendingpoolDepositTxRequest**](LendingpoolDepositTxRequest.md)| Deposit transaction request, if amount is not provided, it will be calculated based on the token balance | 

### Return type

[**InlineResponse200**](InlineResponse200.md)

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

# **lendingpool_tx_repay_post**
> InlineResponse200 lendingpool_tx_repay_post(lendingpool_repay_tx_request)

Repay to lending pool

Repay to lending pool

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
    api_instance = openapi_client.LendingPoolApi(api_client)
    lendingpool_repay_tx_request = openapi_client.LendingpoolRepayTxRequest() # LendingpoolRepayTxRequest | Repay transaction request, if amount is not provided, it will repay the maximum possible amount

    try:
        # Repay to lending pool
        api_response = api_instance.lendingpool_tx_repay_post(lendingpool_repay_tx_request)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling LendingPoolApi->lendingpool_tx_repay_post: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **lendingpool_repay_tx_request** | [**LendingpoolRepayTxRequest**](LendingpoolRepayTxRequest.md)| Repay transaction request, if amount is not provided, it will repay the maximum possible amount | 

### Return type

[**InlineResponse200**](InlineResponse200.md)

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

# **lendingpool_tx_useassetascollateral_post**
> InlineResponse200 lendingpool_tx_useassetascollateral_post(lendingpool_use_asset_as_collateral_tx_request)

Enable/Disable asset as collateral

Allows to enable/disable a specific asset as collateral

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
    api_instance = openapi_client.LendingPoolApi(api_client)
    lendingpool_use_asset_as_collateral_tx_request = openapi_client.LendingpoolUseAssetAsCollateralTxRequest() # LendingpoolUseAssetAsCollateralTxRequest | UseAssetAsCollateral transaction request

    try:
        # Enable/Disable asset as collateral
        api_response = api_instance.lendingpool_tx_useassetascollateral_post(lendingpool_use_asset_as_collateral_tx_request)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling LendingPoolApi->lendingpool_tx_useassetascollateral_post: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **lendingpool_use_asset_as_collateral_tx_request** | [**LendingpoolUseAssetAsCollateralTxRequest**](LendingpoolUseAssetAsCollateralTxRequest.md)| UseAssetAsCollateral transaction request | 

### Return type

[**InlineResponse200**](InlineResponse200.md)

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

# **lendingpool_tx_withdraw_post**
> InlineResponse200 lendingpool_tx_withdraw_post(lendingpool_withdraw_tx_request)

Withdraw from lending pool

Withdraw from lending pool

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
    api_instance = openapi_client.LendingPoolApi(api_client)
    lendingpool_withdraw_tx_request = openapi_client.LendingpoolWithdrawTxRequest() # LendingpoolWithdrawTxRequest | Withdraw transaction request, if amount is not provided, it will be calculated based on the user account status

    try:
        # Withdraw from lending pool
        api_response = api_instance.lendingpool_tx_withdraw_post(lendingpool_withdraw_tx_request)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling LendingPoolApi->lendingpool_tx_withdraw_post: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **lendingpool_withdraw_tx_request** | [**LendingpoolWithdrawTxRequest**](LendingpoolWithdrawTxRequest.md)| Withdraw transaction request, if amount is not provided, it will be calculated based on the user account status | 

### Return type

[**InlineResponse200**](InlineResponse200.md)

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

