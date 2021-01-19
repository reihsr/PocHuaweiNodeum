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

# https://github.com/nodeum-io/nodeum-sdk-python/blob/master/docs/TasksApi.md

print("----- index_tasks -----")
with nodeum_sdk.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = nodeum_sdk.TasksApi(api_client)
    try:
        # Lists all tasks.
        api_response = api_instance.index_tasks()
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling TasksApi->index_tasks: %s\n" % e)

print("----- run_task_result -----")
with nodeum_sdk.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = nodeum_sdk.TasksApi(api_client)
    task_id = 1
    job_id = 1
    try:
        # Check result of a task run request.
        api_response = api_instance.run_task_result(task_id=task_id, job_id=job_id)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling TasksApi->run_task_result: %s\n" % e)

print("----- show_task -----")
with nodeum_sdk.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = nodeum_sdk.TasksApi(api_client)
    task_id = 1
    try:
        # Check result of a task run request.
        api_response = api_instance.show_task(task_id=task_id)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling TasksApi->run_task_result: %s\n" % e)

print("----- Displays the task schedule -----")
with nodeum_sdk.ApiClient(configuration) as api_client:
    api_instance = nodeum_sdk.TaskSchedulesApi(api_client)
    task_id = 'Transfere-Scanner-to-Buffer-Storage'
    try:
        # Displays the task schedule.
        api_response = api_instance.show_task_schedule(task_id=task_id)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling TaskSchedulesApi->show_task_schedule: %s\n" % e)