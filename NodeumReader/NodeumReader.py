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

with nodeum_sdk.ApiClient(configuration) as api_client:
    api_instance = nodeum_sdk.TaskSchedulesApi(api_client)
    task_id = 'Transfere-Scanner-to-Buffer-Storage'
    try:
        # Displays the task schedule.
        api_response = api_instance.show_task_schedule(task_id=task_id)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling TaskSchedulesApi->show_task_schedule: %s\n" % e)

with nodeum_sdk.ApiClient(configuration) as api_client:
    api_instance = nodeum_sdk.FilesApi(api_client)
    task_id = 'Transfere-Scanner-to-Buffer-Storage'

    print("-----------------")

    try:
        # Lists files on root.
        api_response = api_instance.index_files_by_task(task_id=task_id)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling FilesApi->index_files_by_task: %s\n" % e)

    print("-----------------")

    try:
        # Lists files on root.
        api_response = api_instance.index_files()
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling FilesApi->index_files: %s\n" % e)

    print("-----------------")

    task_execution_id = '1606751746229517672'
    try:
        # Lists files on root.
        api_response = api_instance.index_files_by_task_execution(task_execution_id=task_execution_id)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling FilesApi->index_files_by_task_execution: %s\n" % e)

    print("-----------------")

    task_execution_id = '1606751746229517672'
    file_parent_id= '2'

    try:
        # Lists files under a specific folder.
        api_response = api_instance.files_children_by_task_execution(task_execution_id=task_execution_id, file_parent_id=file_parent_id)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling FilesApi->files_children_by_task_execution: %s\n" % e)

print("----------------- TaskExecutionsApi -----------------")

with nodeum_sdk.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = nodeum_sdk.TaskExecutionsApi(api_client)

    try:
        # Lists all task executions.
        api_response = api_instance.index_task_executions()
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling TaskExecutionsApi->index_task_executions: %s\n" % e)
