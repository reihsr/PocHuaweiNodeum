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

#https://github.com/nodeum-io/nodeum-sdk-python/blob/master/docs/FilesApi.md#files_children
# Enter a context with an instance of the API client
with nodeum_sdk.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = nodeum_sdk.FilesApi(api_client)

    print("----- files_children -----")
    file_parent_id = 1
    try:
        # Lists files under a specific folder.
        api_response = api_instance.files_children(file_parent_id=file_parent_id)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling FilesApi->files_children: %s\n" % e)

    print("----- files_children_by_container -----")
    container_id = 1
    file_parent_id = 1
    try:
        # Lists files under a specific folder.
        api_response = api_instance.files_children_by_container(container_id=container_id, file_parent_id=file_parent_id)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling FilesApi->files_children_by_container: %s\n" % e)

    print("----- files_children_by_container -----")
    pool_id = 1
    file_parent_id = 1
    try:
        # Lists files under a specific folder.
        api_response = api_instance.files_children_by_pool(pool_id=pool_id, file_parent_id=file_parent_id)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling FilesApi->files_children_by_pool: %s\n" % e)

    print("----- files_children_by_task -----")
    task_id=2
    file_parent_id=1
    try:
        # Lists files under a specific folder.
        api_response = api_instance.files_children_by_task(task_id=task_id, file_parent_id=file_parent_id)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling FilesApi->files_children_by_task: %s\n" % e)

    print("----- files_children_by_task_execution -----")
    task_execution_id=1
    file_parent_id=1
    try:
        # Lists files under a specific folder.
        api_response = api_instance.files_children_by_task_execution(task_execution_id=task_execution_id, file_parent_id=file_parent_id)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling FilesApi->files_children_by_task_execution: %s\n" % e)

    print("----- files_children_by_task_execution -----")
    task_id=1
    task_execution_id=1
    file_parent_id=1
    try:
        # Lists files under a specific folder.
        api_response = api_instance.files_children_by_task_execution_by_task(task_id=task_id, task_execution_id=task_execution_id, file_parent_id=file_parent_id)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling FilesApi->files_children_by_task_execution_by_task: %s\n" % e)

    print("----- import_files_children_by_pool -----")
    pool_id=1
    file_parent_id=1
    try:
        # Lists files under a specific folder on tape of pools, specific for Data Exchange.
        api_response = api_instance.import_files_children_by_pool(pool_id=pool_id, file_parent_id=file_parent_id)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling FilesApi->import_files_children_by_pool: %s\n" % e)

    print("----- index_files -----")
    try:
        # Lists files on root.
        api_response = api_instance.index_files()
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling FilesApi->index_files: %s\n" % e)

    print("----- index_files_by_task -----")
    task_id=1
    try:
        # Lists files on root.
        api_response = api_instance.index_files_by_task(task_id=task_id)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling FilesApi->index_files_by_task: %s\n" % e)

    print("----- files_children_by_task -----")
    task_id = 1
    file_parent_id = 5
    try:
        # Lists files under a specific folder.
        api_response = api_instance.files_children_by_task(task_id=task_id, file_parent_id=file_parent_id)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling FilesApi->files_children_by_task: %s\n" % e)

    print("----- files_children_by_task -----")
    task_id = 1
    file_parent_id = 6
    try:
        # Lists files under a specific folder.
        api_response = api_instance.files_children_by_task(task_id=task_id, file_parent_id=file_parent_id)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling FilesApi->files_children_by_task: %s\n" % e)

    print("----- show_file -----")
    file_id=9
    try:
        # Displays a specific file.
        api_response = api_instance.show_file(file_id=file_id)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling FilesApi->show_file: %s\n" % e)

    print("----- show_file -----")
    file_id = 9
    task_id = 1
    try:
        # Displays a specific file.
        api_response = api_instance.show_file_by_task(task_id=task_id, file_id=file_id)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling FilesApi->show_file_by_task: %s\n" % e)
