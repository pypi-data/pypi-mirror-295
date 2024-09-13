# ContractResponsePagedResponse


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**page** | **int** |  | [optional] [readonly] 
**page_size** | **int** |  | [optional] [readonly] 
**total_items** | **int** |  | [optional] [readonly] 
**total_pages** | **int** |  | [optional] [readonly] 
**data** | [**List[ContractResponse]**](ContractResponse.md) |  | [optional] [readonly] 

## Example

```python
from redrover_api.models.contract_response_paged_response import ContractResponsePagedResponse

# TODO update the JSON string below
json = "{}"
# create an instance of ContractResponsePagedResponse from a JSON string
contract_response_paged_response_instance = ContractResponsePagedResponse.from_json(json)
# print the JSON string representation of the object
print ContractResponsePagedResponse.to_json()

# convert the object into a dict
contract_response_paged_response_dict = contract_response_paged_response_instance.to_dict()
# create an instance of ContractResponsePagedResponse from a dict
contract_response_paged_response_form_dict = contract_response_paged_response.from_dict(contract_response_paged_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


