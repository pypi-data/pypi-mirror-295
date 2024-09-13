# LocationRequest


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**address** | [**AddressRequest**](AddressRequest.md) |  | 
**notes** | **str** | Notes about the location. | [optional] 
**code** | **str** | The code of the location. | [optional] 
**location_group_id** | [**Int32LocatorRequest**](Int32LocatorRequest.md) |  | [optional] 
**available_to_hiring** | **bool** | Indicator as to whether or not the location is available for hiring. If not value is provided, AvailableToHiring will default to &#39;false&#39; | [optional] 
**phone_number** | **str** | The phone number of the location. | [optional] 
**time_zone** | **int** |  | [optional] 
**name** | **str** | The name of object | 
**external_id** | **str** | The external ID of object (alpha-numeric) | [optional] 

## Example

```python
from redrover_api.models.location_request import LocationRequest

# TODO update the JSON string below
json = "{}"
# create an instance of LocationRequest from a JSON string
location_request_instance = LocationRequest.from_json(json)
# print the JSON string representation of the object
print LocationRequest.to_json()

# convert the object into a dict
location_request_dict = location_request_instance.to_dict()
# create an instance of LocationRequest from a dict
location_request_form_dict = location_request.from_dict(location_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


