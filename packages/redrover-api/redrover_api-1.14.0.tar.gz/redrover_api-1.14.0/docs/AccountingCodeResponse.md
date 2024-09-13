# AccountingCodeResponse

The Accounting code that is associated with the Vacancy

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**locations** | [**List[Int32IdNameClass]**](Int32IdNameClass.md) | List of locations that the Accounting Code is associated with | [optional] 
**all_locations** | **bool** | Indicates if the Accounting Code is associated with all locations | [optional] 
**code** | **str** | The Code used | [optional] [readonly] 
**name** | **str** |  | [optional] 
**id** | **int** |  | [optional] 
**external_id** | **str** |  | [optional] 

## Example

```python
from redrover_api.models.accounting_code_response import AccountingCodeResponse

# TODO update the JSON string below
json = "{}"
# create an instance of AccountingCodeResponse from a JSON string
accounting_code_response_instance = AccountingCodeResponse.from_json(json)
# print the JSON string representation of the object
print AccountingCodeResponse.to_json()

# convert the object into a dict
accounting_code_response_dict = accounting_code_response_instance.to_dict()
# create an instance of AccountingCodeResponse from a dict
accounting_code_response_form_dict = accounting_code_response.from_dict(accounting_code_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


