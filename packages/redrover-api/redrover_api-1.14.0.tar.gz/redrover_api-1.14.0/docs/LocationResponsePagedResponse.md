# LocationResponsePagedResponse


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**page** | **int** |  | [optional] [readonly] 
**page_size** | **int** |  | [optional] [readonly] 
**total_items** | **int** |  | [optional] [readonly] 
**total_pages** | **int** |  | [optional] [readonly] 
**data** | [**List[LocationResponse]**](LocationResponse.md) |  | [optional] [readonly] 

## Example

```python
from redrover_api.models.location_response_paged_response import LocationResponsePagedResponse

# TODO update the JSON string below
json = "{}"
# create an instance of LocationResponsePagedResponse from a JSON string
location_response_paged_response_instance = LocationResponsePagedResponse.from_json(json)
# print the JSON string representation of the object
print LocationResponsePagedResponse.to_json()

# convert the object into a dict
location_response_paged_response_dict = location_response_paged_response_instance.to_dict()
# create an instance of LocationResponsePagedResponse from a dict
location_response_paged_response_form_dict = location_response_paged_response.from_dict(location_response_paged_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


