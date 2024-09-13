# ContractResponse

Contract

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**number_of_days** | **int** | The duration in days of the contract | [optional] 
**days_to_work** | [**List[DayOfWeek]**](DayOfWeek.md) |  | [optional] 
**work_day_pattern** | [**Int32IdNameClass**](Int32IdNameClass.md) |  | [optional] 
**pay_cycle** | [**Int32IdNameClass**](Int32IdNameClass.md) |  | [optional] 
**time_settings** | [**TimeSettingsResponse**](TimeSettingsResponse.md) |  | [optional] 
**valid_until_utc** | **datetime** |  | [optional] 
**name** | **str** |  | [optional] 
**id** | **int** |  | [optional] 
**external_id** | **str** |  | [optional] 

## Example

```python
from redrover_api.models.contract_response import ContractResponse

# TODO update the JSON string below
json = "{}"
# create an instance of ContractResponse from a JSON string
contract_response_instance = ContractResponse.from_json(json)
# print the JSON string representation of the object
print ContractResponse.to_json()

# convert the object into a dict
contract_response_dict = contract_response_instance.to_dict()
# create an instance of ContractResponse from a dict
contract_response_form_dict = contract_response.from_dict(contract_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


