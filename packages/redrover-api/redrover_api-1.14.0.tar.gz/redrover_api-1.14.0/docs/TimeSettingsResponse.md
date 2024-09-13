# TimeSettingsResponse


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **int** | The unique identifier for the time settings object. | [optional] 
**time_tracking_source_types** | **List[int]** | The source from which time tracking data is obtained. It could be from a kiosk clock, an application clock, or manual entry. It can also be a combination of these sources. | [optional] 
**time_tracking_mode** | **int** |  | [optional] 
**warn_if_manual_time_entry** | **bool** | A flag that triggers a warning if time entries are manually entered. | [optional] 
**allow_time_durations_only** | **bool** | A flag that allows only time durations to be entered. | [optional] 
**allow_break_time_durations_only** | **bool** | A flag that allows only break time durations to be entered. | [optional] 
**allow_multiple_breaks** | **bool** | A flag that allows multiple breaks to be entered. | [optional] 
**hide_breaks_on_clock** | **bool** | A flag that hides breaks on the clock. | [optional] 
**ignore_ip_restrictions** | **bool** | A flag that ignores IP restrictions. | [optional] 

## Example

```python
from redrover_api.models.time_settings_response import TimeSettingsResponse

# TODO update the JSON string below
json = "{}"
# create an instance of TimeSettingsResponse from a JSON string
time_settings_response_instance = TimeSettingsResponse.from_json(json)
# print the JSON string representation of the object
print TimeSettingsResponse.to_json()

# convert the object into a dict
time_settings_response_dict = time_settings_response_instance.to_dict()
# create an instance of TimeSettingsResponse from a dict
time_settings_response_form_dict = time_settings_response.from_dict(time_settings_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


