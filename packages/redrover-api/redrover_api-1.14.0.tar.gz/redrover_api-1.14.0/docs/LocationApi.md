# redrover_api.LocationApi

All URIs are relative to *http://localhost*

Method | HTTP request | Description
------------- | ------------- | -------------
[**create_location**](LocationApi.md#create_location) | **POST** /api/v1/{orgId}/Location | Create a new location
[**delete_location**](LocationApi.md#delete_location) | **DELETE** /api/v1/{orgId}/Location/{identifier} | Delete a location
[**get_location**](LocationApi.md#get_location) | **GET** /api/v1/{orgId}/Location/{identifier} | Get location by identifier
[**get_locations**](LocationApi.md#get_locations) | **GET** /api/v1/{orgId}/Location | Get paged list of locations
[**update_location**](LocationApi.md#update_location) | **PUT** /api/v1/{orgId}/Location/{identifier} | Update an existing location


# **create_location**
> LocationResponse create_location(org_id, location_request)

Create a new location

Create a new location for an organization.

### Example

* Basic Authentication (basic):

```python
import time
import os
import redrover_api
from redrover_api.models.location_request import LocationRequest
from redrover_api.models.location_response import LocationResponse
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
    api_instance = redrover_api.LocationApi(api_client)
    org_id = 56 # int | The Red Rover Id of the Organization
    location_request = redrover_api.LocationRequest() # LocationRequest | The details of the location

    try:
        # Create a new location
        api_response = api_instance.create_location(org_id, location_request)
        print("The response of LocationApi->create_location:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling LocationApi->create_location: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **org_id** | **int**| The Red Rover Id of the Organization | 
 **location_request** | [**LocationRequest**](LocationRequest.md)| The details of the location | 

### Return type

[**LocationResponse**](LocationResponse.md)

### Authorization

[basic](../README.md#basic)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**201** | Location created |  -  |
**401** | Unauthorized |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **delete_location**
> OkResult delete_location(org_id, identifier)

Delete a location

Delete an existing location by it's identifier.

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
    api_instance = redrover_api.LocationApi(api_client)
    org_id = 56 # int | The Red Rover Id of the Organization
    identifier = 'identifier_example' # str | The identifier of the Location. If this is an External Id, prepend the value with the pipe character `|` (e.g. `|ABC123`)

    try:
        # Delete a location
        api_response = api_instance.delete_location(org_id, identifier)
        print("The response of LocationApi->delete_location:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling LocationApi->delete_location: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **org_id** | **int**| The Red Rover Id of the Organization | 
 **identifier** | **str**| The identifier of the Location. If this is an External Id, prepend the value with the pipe character &#x60;|&#x60; (e.g. &#x60;|ABC123&#x60;) | 

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
**200** | Deletes the location |  -  |
**401** | Unauthorized |  -  |
**404** | Organization not found. Location not found or has already been deleted |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_location**
> LocationResponse get_location(org_id, identifier)

Get location by identifier

Get a specific location by it's identifier.

### Example

* Basic Authentication (apiKey):

```python
import time
import os
import redrover_api
from redrover_api.models.location_response import LocationResponse
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
    api_instance = redrover_api.LocationApi(api_client)
    org_id = 56 # int | The Red Rover Id of the Organization
    identifier = 'identifier_example' # str | The identifier of the Location. If this is an External Id, prepend the value with the pipe character `|` (e.g. `|ABC123`)

    try:
        # Get location by identifier
        api_response = api_instance.get_location(org_id, identifier)
        print("The response of LocationApi->get_location:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling LocationApi->get_location: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **org_id** | **int**| The Red Rover Id of the Organization | 
 **identifier** | **str**| The identifier of the Location. If this is an External Id, prepend the value with the pipe character &#x60;|&#x60; (e.g. &#x60;|ABC123&#x60;) | 

### Return type

[**LocationResponse**](LocationResponse.md)

### Authorization

[apiKey](../README.md#apiKey)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Gets location |  -  |
**401** | Unauthorized |  -  |
**404** | Locations not found or has been deleted |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_locations**
> LocationResponsePagedResponse get_locations(org_id, page, page_size)

Get paged list of locations

Get a paged list of locations for an Organization

### Example

* Basic Authentication (apiKey):

```python
import time
import os
import redrover_api
from redrover_api.models.location_response_paged_response import LocationResponsePagedResponse
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
    api_instance = redrover_api.LocationApi(api_client)
    org_id = 56 # int | The Red Rover Id of the Organization
    page = 1 # int | Page number to return (default to 1)
    page_size = 10 # int | Number of Locations to include per page (default to 10)

    try:
        # Get paged list of locations
        api_response = api_instance.get_locations(org_id, page, page_size)
        print("The response of LocationApi->get_locations:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling LocationApi->get_locations: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **org_id** | **int**| The Red Rover Id of the Organization | 
 **page** | **int**| Page number to return | [default to 1]
 **page_size** | **int**| Number of Locations to include per page | [default to 10]

### Return type

[**LocationResponsePagedResponse**](LocationResponsePagedResponse.md)

### Authorization

[apiKey](../README.md#apiKey)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Gets locations |  -  |
**401** | Unauthorized |  -  |
**404** | Locations not found or has been deleted |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **update_location**
> LocationResponse update_location(org_id, identifier, location_update_request)

Update an existing location

Update details an existing location.

### Example

* Basic Authentication (apiKey):

```python
import time
import os
import redrover_api
from redrover_api.models.location_response import LocationResponse
from redrover_api.models.location_update_request import LocationUpdateRequest
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
    api_instance = redrover_api.LocationApi(api_client)
    org_id = 56 # int | The Red Rover Id of the Organization
    identifier = 'identifier_example' # str | The identifier of the Location. If this is an External Id, prepend the value with the pipe character `|` (e.g. `|ABC123`)
    location_update_request = redrover_api.LocationUpdateRequest() # LocationUpdateRequest | The Location Payload

    try:
        # Update an existing location
        api_response = api_instance.update_location(org_id, identifier, location_update_request)
        print("The response of LocationApi->update_location:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling LocationApi->update_location: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **org_id** | **int**| The Red Rover Id of the Organization | 
 **identifier** | **str**| The identifier of the Location. If this is an External Id, prepend the value with the pipe character &#x60;|&#x60; (e.g. &#x60;|ABC123&#x60;) | 
 **location_update_request** | [**LocationUpdateRequest**](LocationUpdateRequest.md)| The Location Payload | 

### Return type

[**LocationResponse**](LocationResponse.md)

### Authorization

[apiKey](../README.md#apiKey)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Location updated |  -  |
**201** | Location created if it previously did not exist |  -  |
**400** | Location already exists. Invalid input |  -  |
**401** | Unauthorized |  -  |
**404** | Organization not found. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

