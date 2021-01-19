from __future__ import print_function
import time
import nodeum_sdk
from nodeum_sdk.rest import ApiException
from pprint import pprint
from jproperties import Properties

configuration = nodeum_sdk.Configuration()
configs = Properties()

with open('..\config.properties', 'rb') as config_file:
    configs.load(config_file)

configuration.username = configs.get("NODEUM_User").data
configuration.password = configs.get("NODEUM_PWD").data
configuration.host = "http://" + configs.get("NODEUM_HOST").data + "/api/v2"

#https://github.com/nodeum-io/nodeum-sdk-python/blob/master/docs/MetadataApi.md#index_file_metadata_definitions
# Enter a context with an instance of the API client
with nodeum_sdk.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = nodeum_sdk.MetadataApi(api_client)

    print("----- index_file_metadata_definitions -----")
    try:
        # List file metadata definitions
        api_response = api_instance.index_file_metadata_definitions()
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling MetadataApi->index_file_metadata_definitions: %s\n" % e)

    print("----- index_task_metadata_definitions -----")
    try:
        # List task metadata definitions
        api_response = api_instance.index_task_metadata_definitions()
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling MetadataApi->index_task_metadata_definitions: %s\n" % e)

    print("----- show_file_metadata_definition -----")
    metadata_definition_id=1
    try:
        # Displays a specific task metadata definition.
        api_response = api_instance.show_file_metadata_definition(metadata_definition_id=metadata_definition_id)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling MetadataApi->show_file_metadata_definition: %s\n" % e)

    print("----- show_file_metadata_definition -----")
    metadata_definition_id = 1
    try:
        # Displays a specific task metadata definition.
        api_response = api_instance.show_task_metadata_definition(metadata_definition_id)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling MetadataApi->show_task_metadata_definition: %s\n" % e)