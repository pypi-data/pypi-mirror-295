# redrover_api.ContractApi

All URIs are relative to *http://localhost*

Method | HTTP request | Description
------------- | ------------- | -------------
[**create_contract**](ContractApi.md#create_contract) | **POST** /api/v1/{orgId}/Contract | Create new Contract
[**delete_contract**](ContractApi.md#delete_contract) | **DELETE** /api/v1/{orgId}/Contract/{identifier} | Delete a contract
[**get_contract**](ContractApi.md#get_contract) | **GET** /api/v1/{orgId}/Contract/{identifier} | Get Contract
[**get_contracts**](ContractApi.md#get_contracts) | **GET** /api/v1/{orgId}/Contract | Get a paged list of contracts
[**update_contract**](ContractApi.md#update_contract) | **PUT** /api/v1/{orgId}/Contract | Update an existing Contract


# **create_contract**
> ContractResponse create_contract(org_id, contract_create_request)

Create new Contract

Create a contract for an Organization

### Example

* Basic Authentication (apiKey):

```python
import time
import os
import redrover_api
from redrover_api.models.contract_create_request import ContractCreateRequest
from redrover_api.models.contract_response import ContractResponse
from redrover_api.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = redrover_api.Configuration(
    host = "http://localhost"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure HTTP basic authorization: apiKey
configuration = redrover_api.Configuration(
    username = os.environ["USERNAME"],
    password = os.environ["PASSWORD"]
)

# Enter a context with an instance of the API client
with redrover_api.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = redrover_api.ContractApi(api_client)
    org_id = 56 # int | The Red Rover Id of the Organization
    contract_create_request = redrover_api.ContractCreateRequest() # ContractCreateRequest | The details of the Contract

    try:
        # Create new Contract
        api_response = api_instance.create_contract(org_id, contract_create_request)
        print("The response of ContractApi->create_contract:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ContractApi->create_contract: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **org_id** | **int**| The Red Rover Id of the Organization | 
 **contract_create_request** | [**ContractCreateRequest**](ContractCreateRequest.md)| The details of the Contract | 

### Return type

[**ContractResponse**](ContractResponse.md)

### Authorization

[apiKey](../README.md#apiKey)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Contract created |  -  |
**400** | Contract already exists. Invalid input |  -  |
**401** | Unauthorized |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **delete_contract**
> OkResult delete_contract(org_id, identifier)

Delete a contract

Delete an existing contract based on it's identifier

### Example

* Basic Authentication (apiKey):

```python
import time
import os
import redrover_api
from redrover_api.models.ok_result import OkResult
from redrover_api.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = redrover_api.Configuration(
    host = "http://localhost"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure HTTP basic authorization: apiKey
configuration = redrover_api.Configuration(
    username = os.environ["USERNAME"],
    password = os.environ["PASSWORD"]
)

# Enter a context with an instance of the API client
with redrover_api.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = redrover_api.ContractApi(api_client)
    org_id = 56 # int | The Red Rover Id of the Organization
    identifier = 'identifier_example' # str | The identifier of the Contract. If this is an External Id, prepend the value with the pipe character `|` (e.g. `|ABC123`)

    try:
        # Delete a contract
        api_response = api_instance.delete_contract(org_id, identifier)
        print("The response of ContractApi->delete_contract:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ContractApi->delete_contract: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **org_id** | **int**| The Red Rover Id of the Organization | 
 **identifier** | **str**| The identifier of the Contract. If this is an External Id, prepend the value with the pipe character &#x60;|&#x60; (e.g. &#x60;|ABC123&#x60;) | 

### Return type

[**OkResult**](OkResult.md)

### Authorization

[apiKey](../README.md#apiKey)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Deletes the Contract |  -  |
**401** | Unauthorized |  -  |
**404** | Organization not found. Contract not found or has already been deleted |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_contract**
> ContractResponse get_contract(org_id, identifier)

Get Contract

Get a specific contract by it's identifier.

### Example

* Basic Authentication (apiKey):

```python
import time
import os
import redrover_api
from redrover_api.models.contract_response import ContractResponse
from redrover_api.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = redrover_api.Configuration(
    host = "http://localhost"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure HTTP basic authorization: apiKey
configuration = redrover_api.Configuration(
    username = os.environ["USERNAME"],
    password = os.environ["PASSWORD"]
)

# Enter a context with an instance of the API client
with redrover_api.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = redrover_api.ContractApi(api_client)
    org_id = 56 # int | The Red Rover Id of the Organization
    identifier = 'identifier_example' # str | The identifier of the Contract. If this is an External Id, prepend the value with the pipe character `|` (e.g. `|ABC123`)

    try:
        # Get Contract
        api_response = api_instance.get_contract(org_id, identifier)
        print("The response of ContractApi->get_contract:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ContractApi->get_contract: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **org_id** | **int**| The Red Rover Id of the Organization | 
 **identifier** | **str**| The identifier of the Contract. If this is an External Id, prepend the value with the pipe character &#x60;|&#x60; (e.g. &#x60;|ABC123&#x60;) | 

### Return type

[**ContractResponse**](ContractResponse.md)

### Authorization

[apiKey](../README.md#apiKey)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Gets Contract |  -  |
**401** | Unauthorized |  -  |
**404** | Contracts not found or has been deleted |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_contracts**
> ContractResponsePagedResponse get_contracts(org_id, page, page_size)

Get a paged list of contracts

Get a paged list of contracts in an Organization

### Example

* Basic Authentication (apiKey):

```python
import time
import os
import redrover_api
from redrover_api.models.contract_response_paged_response import ContractResponsePagedResponse
from redrover_api.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = redrover_api.Configuration(
    host = "http://localhost"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure HTTP basic authorization: apiKey
configuration = redrover_api.Configuration(
    username = os.environ["USERNAME"],
    password = os.environ["PASSWORD"]
)

# Enter a context with an instance of the API client
with redrover_api.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = redrover_api.ContractApi(api_client)
    org_id = 56 # int | The Red Rover Id of the Organization
    page = 1 # int | Page number to return (default to 1)
    page_size = 10 # int | Number of Copntracts to include per page (default to 10)

    try:
        # Get a paged list of contracts
        api_response = api_instance.get_contracts(org_id, page, page_size)
        print("The response of ContractApi->get_contracts:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ContractApi->get_contracts: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **org_id** | **int**| The Red Rover Id of the Organization | 
 **page** | **int**| Page number to return | [default to 1]
 **page_size** | **int**| Number of Copntracts to include per page | [default to 10]

### Return type

[**ContractResponsePagedResponse**](ContractResponsePagedResponse.md)

### Authorization

[apiKey](../README.md#apiKey)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Gets a paged list of Contracts |  -  |
**401** | Unauthorized |  -  |
**404** | Contracts not found or has been deleted |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **update_contract**
> ContractResponse update_contract(org_id, identifier, contract_update_request)

Update an existing Contract

Update details an already existing contract for an Organization

### Example

* Basic Authentication (apiKey):

```python
import time
import os
import redrover_api
from redrover_api.models.contract_response import ContractResponse
from redrover_api.models.contract_update_request import ContractUpdateRequest
from redrover_api.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = redrover_api.Configuration(
    host = "http://localhost"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure HTTP basic authorization: apiKey
configuration = redrover_api.Configuration(
    username = os.environ["USERNAME"],
    password = os.environ["PASSWORD"]
)

# Enter a context with an instance of the API client
with redrover_api.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = redrover_api.ContractApi(api_client)
    org_id = 56 # int | The Red Rover Id of the Organization
    identifier = 'identifier_example' # str | The identifier of the Contract. If this is an External Id, prepend the value with the pipe character `|` (e.g. `|ABC123`)
    contract_update_request = redrover_api.ContractUpdateRequest() # ContractUpdateRequest | The details of the Contract

    try:
        # Update an existing Contract
        api_response = api_instance.update_contract(org_id, identifier, contract_update_request)
        print("The response of ContractApi->update_contract:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ContractApi->update_contract: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **org_id** | **int**| The Red Rover Id of the Organization | 
 **identifier** | **str**| The identifier of the Contract. If this is an External Id, prepend the value with the pipe character &#x60;|&#x60; (e.g. &#x60;|ABC123&#x60;) | 
 **contract_update_request** | [**ContractUpdateRequest**](ContractUpdateRequest.md)| The details of the Contract | 

### Return type

[**ContractResponse**](ContractResponse.md)

### Authorization

[apiKey](../README.md#apiKey)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Contract updated |  -  |
**201** | Contract created if it previously did not exist |  -  |
**400** | Contract already exists. Invalid input |  -  |
**401** | Unauthorized |  -  |
**404** | Organization not found. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

