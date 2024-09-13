# redrover_api.AccountingCodeApi

All URIs are relative to *http://localhost*

Method | HTTP request | Description
------------- | ------------- | -------------
[**create_accounting_code**](AccountingCodeApi.md#create_accounting_code) | **POST** /api/v1/{orgId}/AccountingCode | Create a new accounting code
[**delete_accounting_code**](AccountingCodeApi.md#delete_accounting_code) | **DELETE** /api/v1/{orgId}/AccountingCode/{identifier} | Delete an accounting code
[**get_accounting_code**](AccountingCodeApi.md#get_accounting_code) | **GET** /api/v1/{orgId}/AccountingCode/{identifier} | Get accounting code
[**get_accounting_codes**](AccountingCodeApi.md#get_accounting_codes) | **GET** /api/v1/{orgId}/AccountingCode | Get paged list of accounting codes
[**update_accounting_code**](AccountingCodeApi.md#update_accounting_code) | **PUT** /api/v1/{orgId}/AccountingCode/{identifier} | Update an existing accounting code


# **create_accounting_code**
> AccountingCodeResponse create_accounting_code(org_id, accounting_code_request)

Create a new accounting code

Create a new accounting code in an organization.

### Example

* Basic Authentication (basic):

```python
import time
import os
import redrover_api
from redrover_api.models.accounting_code_request import AccountingCodeRequest
from redrover_api.models.accounting_code_response import AccountingCodeResponse
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

# Configure HTTP basic authorization: basic
configuration = redrover_api.Configuration(
    username = os.environ["USERNAME"],
    password = os.environ["PASSWORD"]
)

# Enter a context with an instance of the API client
with redrover_api.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = redrover_api.AccountingCodeApi(api_client)
    org_id = 56 # int | The Red Rover Id of the Organization
    accounting_code_request = redrover_api.AccountingCodeRequest() # AccountingCodeRequest | The details of the accounting code

    try:
        # Create a new accounting code
        api_response = api_instance.create_accounting_code(org_id, accounting_code_request)
        print("The response of AccountingCodeApi->create_accounting_code:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling AccountingCodeApi->create_accounting_code: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **org_id** | **int**| The Red Rover Id of the Organization | 
 **accounting_code_request** | [**AccountingCodeRequest**](AccountingCodeRequest.md)| The details of the accounting code | 

### Return type

[**AccountingCodeResponse**](AccountingCodeResponse.md)

### Authorization

[basic](../README.md#basic)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**201** | Accounting code created |  -  |
**401** | Unauthorized |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **delete_accounting_code**
> OkResult delete_accounting_code(org_id, identifier)

Delete an accounting code

Delete an existing accounting code by it's identifier.

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
    api_instance = redrover_api.AccountingCodeApi(api_client)
    org_id = 56 # int | The Red Rover Id of the Organization
    identifier = 'identifier_example' # str | The identifier of the AccountingCode. If this is an External Id, prepend the value with the pipe character `|` (e.g. `|ABC123`)

    try:
        # Delete an accounting code
        api_response = api_instance.delete_accounting_code(org_id, identifier)
        print("The response of AccountingCodeApi->delete_accounting_code:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling AccountingCodeApi->delete_accounting_code: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **org_id** | **int**| The Red Rover Id of the Organization | 
 **identifier** | **str**| The identifier of the AccountingCode. If this is an External Id, prepend the value with the pipe character &#x60;|&#x60; (e.g. &#x60;|ABC123&#x60;) | 

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
**200** | Deletes the accounting code |  -  |
**401** | Unauthorized |  -  |
**404** | Organization not found. Accounting code not found or has already been deleted |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_accounting_code**
> AccountingCodeResponse get_accounting_code(org_id, identifier)

Get accounting code

Get a specific accounting code by it's identifier.

### Example

* Basic Authentication (apiKey):

```python
import time
import os
import redrover_api
from redrover_api.models.accounting_code_response import AccountingCodeResponse
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
    api_instance = redrover_api.AccountingCodeApi(api_client)
    org_id = 56 # int | The Red Rover Id of the Organization
    identifier = 'identifier_example' # str | The identifier of the AccountingCode. If this is an External Id, prepend the value with the pipe character `|` (e.g. `|ABC123`)

    try:
        # Get accounting code
        api_response = api_instance.get_accounting_code(org_id, identifier)
        print("The response of AccountingCodeApi->get_accounting_code:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling AccountingCodeApi->get_accounting_code: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **org_id** | **int**| The Red Rover Id of the Organization | 
 **identifier** | **str**| The identifier of the AccountingCode. If this is an External Id, prepend the value with the pipe character &#x60;|&#x60; (e.g. &#x60;|ABC123&#x60;) | 

### Return type

[**AccountingCodeResponse**](AccountingCodeResponse.md)

### Authorization

[apiKey](../README.md#apiKey)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Gets AccountingCode |  -  |
**401** | Unauthorized |  -  |
**404** | AccountingCodes not found or has been deleted |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_accounting_codes**
> AccountingCodeResponsePagedResponse get_accounting_codes(org_id, page, page_size)

Get paged list of accounting codes

Get a paged list of accounting codes in an Organization

### Example

* Basic Authentication (apiKey):

```python
import time
import os
import redrover_api
from redrover_api.models.accounting_code_response_paged_response import AccountingCodeResponsePagedResponse
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
    api_instance = redrover_api.AccountingCodeApi(api_client)
    org_id = 56 # int | The Red Rover Id of the Organization
    page = 1 # int | Page number to return (default to 1)
    page_size = 10 # int | Number of Accounting Codes to include per page (default to 10)

    try:
        # Get paged list of accounting codes
        api_response = api_instance.get_accounting_codes(org_id, page, page_size)
        print("The response of AccountingCodeApi->get_accounting_codes:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling AccountingCodeApi->get_accounting_codes: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **org_id** | **int**| The Red Rover Id of the Organization | 
 **page** | **int**| Page number to return | [default to 1]
 **page_size** | **int**| Number of Accounting Codes to include per page | [default to 10]

### Return type

[**AccountingCodeResponsePagedResponse**](AccountingCodeResponsePagedResponse.md)

### Authorization

[apiKey](../README.md#apiKey)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Gets Accounting Codes |  -  |
**401** | Unauthorized |  -  |
**404** | AccountingCodes not found or has been deleted |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **update_accounting_code**
> AccountingCodeResponse update_accounting_code(org_id, identifier, accounting_code_update_request)

Update an existing accounting code

Update details an existing accounting code.

### Example

* Basic Authentication (apiKey):

```python
import time
import os
import redrover_api
from redrover_api.models.accounting_code_response import AccountingCodeResponse
from redrover_api.models.accounting_code_update_request import AccountingCodeUpdateRequest
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
    api_instance = redrover_api.AccountingCodeApi(api_client)
    org_id = 56 # int | The Red Rover Id of the Organization
    identifier = 'identifier_example' # str | The identifier of the AccountingCode. If this is an External Id, prepend the value with the pipe character `|` (e.g. `|ABC123`)
    accounting_code_update_request = redrover_api.AccountingCodeUpdateRequest() # AccountingCodeUpdateRequest | The AccountingCode Payload

    try:
        # Update an existing accounting code
        api_response = api_instance.update_accounting_code(org_id, identifier, accounting_code_update_request)
        print("The response of AccountingCodeApi->update_accounting_code:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling AccountingCodeApi->update_accounting_code: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **org_id** | **int**| The Red Rover Id of the Organization | 
 **identifier** | **str**| The identifier of the AccountingCode. If this is an External Id, prepend the value with the pipe character &#x60;|&#x60; (e.g. &#x60;|ABC123&#x60;) | 
 **accounting_code_update_request** | [**AccountingCodeUpdateRequest**](AccountingCodeUpdateRequest.md)| The AccountingCode Payload | 

### Return type

[**AccountingCodeResponse**](AccountingCodeResponse.md)

### Authorization

[apiKey](../README.md#apiKey)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | AccountingCode updated |  -  |
**201** | AccountingCode created if it previously did not exist |  -  |
**400** | AccountingCode already exists. Invalid input |  -  |
**401** | Unauthorized |  -  |
**404** | Organization not found. Accounting Code not found. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

