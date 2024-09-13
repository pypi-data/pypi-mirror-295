# AddressRequest


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**address1** | **str** | The street name and number of the location. | [optional] 
**address2** | **str** | Additional street address details (Suite, Building name, etc). | [optional] 
**city** | **str** | The city in which the location exists. | [optional] 
**state** | **int** |  | [optional] 
**postal_code** | **str** | The postal code in which the location exists. | [optional] 
**country** | **int** |  | [optional] 
**longitude** | **float** | Numerical measure of how far north or south the location is from the Equator (in degrees). | [optional] 
**latitude** | **float** | Numerical measure of how far east or west the location is from the Prime Meridian (in degrees). | [optional] 

## Example

```python
from redrover_api.models.address_request import AddressRequest

# TODO update the JSON string below
json = "{}"
# create an instance of AddressRequest from a JSON string
address_request_instance = AddressRequest.from_json(json)
# print the JSON string representation of the object
print AddressRequest.to_json()

# convert the object into a dict
address_request_dict = address_request_instance.to_dict()
# create an instance of AddressRequest from a dict
address_request_form_dict = address_request.from_dict(address_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


