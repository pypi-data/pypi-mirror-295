# ContractUpdateRequest


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**number_of_days** | **int** | The length of the contract in days. | 
**work_day_pattern** | [**Int32LocatorRequest**](Int32LocatorRequest.md) |  | 
**pay_cycle** | [**Int32LocatorRequest**](Int32LocatorRequest.md) |  | [optional] 
**days_to_work** | [**List[DayOfWeek]**](DayOfWeek.md) | The days of the week that work is scheduled. | 
**name** | **str** | The name of object | 
**external_id** | **str** | The external ID of object (alpha-numeric) | [optional] 

## Example

```python
from redrover_api.models.contract_update_request import ContractUpdateRequest

# TODO update the JSON string below
json = "{}"
# create an instance of ContractUpdateRequest from a JSON string
contract_update_request_instance = ContractUpdateRequest.from_json(json)
# print the JSON string representation of the object
print ContractUpdateRequest.to_json()

# convert the object into a dict
contract_update_request_dict = contract_update_request_instance.to_dict()
# create an instance of ContractUpdateRequest from a dict
contract_update_request_form_dict = contract_update_request.from_dict(contract_update_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


