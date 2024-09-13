# LocationResponse

The details of a location belonging to an organization

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**location_group** | [**Int32IdNameClass**](Int32IdNameClass.md) |  | [optional] 
**notes** | **str** | Notes about the location. | [optional] 
**code** | **str** | The location&#39;s code | [optional] 
**available_to_hiring** | **bool** | Indicates if the location is available for hiring. If false, the location will not be available for hiring. | [optional] 
**phone_number** | **str** | The phone number associated with the location | [optional] 
**time_zone** | **int** |  | [optional] 
**valid_until_utc** | **datetime** | The expiration date of the location | [optional] 
**address1** | **str** | The location&#39;s address | [optional] 
**address2** | **str** | The location&#39;s address (continued) | [optional] 
**city** | **str** | The city of the location | [optional] 
**state** | **int** |  | [optional] 
**postal_code** | **str** | The postal code of the location | [optional] 
**country** | **int** |  | [optional] 
**longitude** | **float** | The longitude of the location | [optional] 
**latitude** | **float** | The latitude of the location | [optional] 
**name** | **str** |  | [optional] 
**id** | **int** |  | [optional] 
**external_id** | **str** |  | [optional] 

## Example

```python
from redrover_api.models.location_response import LocationResponse

# TODO update the JSON string below
json = "{}"
# create an instance of LocationResponse from a JSON string
location_response_instance = LocationResponse.from_json(json)
# print the JSON string representation of the object
print LocationResponse.to_json()

# convert the object into a dict
location_response_dict = location_response_instance.to_dict()
# create an instance of LocationResponse from a dict
location_response_form_dict = location_response.from_dict(location_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


