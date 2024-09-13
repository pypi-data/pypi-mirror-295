# AccountingCodeUpdateRequest


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**location** | [**Int32LocatorRequest**](Int32LocatorRequest.md) |  | [optional] 
**locations** | [**List[Int32LocatorRequest]**](Int32LocatorRequest.md) | A list of locations the accounting code is assigned to. If no locations are provided, the accounting code is assigned to all locations. | [optional] 
**all_locations** | **bool** | Indicator if the accounting code is to be assigned to all locations. If true, the Location and Locations properties are ignored. | [optional] 
**name** | **str** | The name of object | 
**external_id** | **str** | The external ID of object (alpha-numeric) | [optional] 

## Example

```python
from redrover_api.models.accounting_code_update_request import AccountingCodeUpdateRequest

# TODO update the JSON string below
json = "{}"
# create an instance of AccountingCodeUpdateRequest from a JSON string
accounting_code_update_request_instance = AccountingCodeUpdateRequest.from_json(json)
# print the JSON string representation of the object
print AccountingCodeUpdateRequest.to_json()

# convert the object into a dict
accounting_code_update_request_dict = accounting_code_update_request_instance.to_dict()
# create an instance of AccountingCodeUpdateRequest from a dict
accounting_code_update_request_form_dict = accounting_code_update_request.from_dict(accounting_code_update_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


