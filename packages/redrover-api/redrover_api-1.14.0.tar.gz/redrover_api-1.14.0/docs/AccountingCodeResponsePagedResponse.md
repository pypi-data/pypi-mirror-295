# AccountingCodeResponsePagedResponse


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**page** | **int** |  | [optional] [readonly] 
**page_size** | **int** |  | [optional] [readonly] 
**total_items** | **int** |  | [optional] [readonly] 
**total_pages** | **int** |  | [optional] [readonly] 
**data** | [**List[AccountingCodeResponse]**](AccountingCodeResponse.md) |  | [optional] [readonly] 

## Example

```python
from redrover_api.models.accounting_code_response_paged_response import AccountingCodeResponsePagedResponse

# TODO update the JSON string below
json = "{}"
# create an instance of AccountingCodeResponsePagedResponse from a JSON string
accounting_code_response_paged_response_instance = AccountingCodeResponsePagedResponse.from_json(json)
# print the JSON string representation of the object
print AccountingCodeResponsePagedResponse.to_json()

# convert the object into a dict
accounting_code_response_paged_response_dict = accounting_code_response_paged_response_instance.to_dict()
# create an instance of AccountingCodeResponsePagedResponse from a dict
accounting_code_response_paged_response_form_dict = accounting_code_response_paged_response.from_dict(accounting_code_response_paged_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


