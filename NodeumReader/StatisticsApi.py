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

#https://github.com/nodeum-io/nodeum-sdk-python/blob/master/docs/StatisticsApi.md#statistics_by_date
# Enter a context with an instance of the API client
with nodeum_sdk.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = nodeum_sdk.StatisticsApi(api_client)

    print("----- index_file_metadata_definitions -----")
    try:
        # Get statistics about files, grouped by date
        api_response = api_instance.statistics_by_date()
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling StatisticsApi->statistics_by_date: %s\n" % e)

    print("----- statistics_by_file_extension -----")
    try:
        # Get statistics about files, grouped by file extension
        api_response = api_instance.statistics_by_file_extension()
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling StatisticsApi->statistics_by_file_extension: %s\n" % e)

    print("----- statistics_by_group_owner -----")
    try:
        # Get statistics about files, grouped by owner (group)
        api_response = api_instance.statistics_by_group_owner()
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling StatisticsApi->statistics_by_group_owner: %s\n" % e)

    print("----- statistics_by_metadata -----")
    try:
        # Get statistics about files, grouped by metadata
        api_response = api_instance.statistics_by_metadata()
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling StatisticsApi->statistics_by_metadata: %s\n" % e)

    print("----- statistics_by_primary_cloud -----")
    try:
        # Get statistics about files, grouped by primary Cloud
        api_response = api_instance.statistics_by_primary_cloud()
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling StatisticsApi->statistics_by_primary_cloud: %s\n" % e)

    print("----- statistics_by_primary_name -----")
    try:
        # Get statistics about files, grouped by primary storages
        api_response = api_instance.statistics_by_primary_name()
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling StatisticsApi->statistics_by_primary_name: %s\n" % e)

    print("----- statistics_by_primary_nas -----")
    try:
        # Get statistics about files, grouped by primary NAS
        api_response = api_instance.statistics_by_primary_nas()
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling StatisticsApi->statistics_by_primary_nas: %s\n" % e)

    print("----- statistics_by_primary_storage -----")
    try:
        # Get statistics about files, grouped by primary storage
        api_response = api_instance.statistics_by_primary_storage()
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling StatisticsApi->statistics_by_primary_storage: %s\n" % e)

    print("----- statistics_by_secondary_cloud -----")
    try:
        # Get statistics about files, grouped by secondary Cloud
        api_response = api_instance.statistics_by_secondary_cloud()
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling StatisticsApi->statistics_by_secondary_cloud: %s\n" % e)

    print("----- statistics_by_secondary_nas -----")
    try:
        # Get statistics about files, grouped by secondary NAS
        api_response = api_instance.statistics_by_secondary_nas()
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling StatisticsApi->statistics_by_secondary_nas: %s\n" % e)

    print("----- statistics_by_secondary_storage -----")
    try:
        # Get statistics about files, grouped by secondary storage
        api_response = api_instance.statistics_by_secondary_storage()
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling StatisticsApi->statistics_by_secondary_storage: %s\n" % e)

    print("----- statistics_by_size -----")
    try:
        # Get statistics about files, grouped by size
        api_response = api_instance.statistics_by_size()
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling StatisticsApi->statistics_by_size: %s\n" % e)

    print("----- statistics_by_user_owner -----")
    try:
        # Get statistics about files, grouped by owner (user)
        api_response = api_instance.statistics_by_user_owner()
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling StatisticsApi->statistics_by_user_owner: %s\n" % e)

    print("----- statistics_storage -----")
    try:
        # Get statistics about storages, grouped by types
        api_response = api_instance.statistics_storage()
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling StatisticsApi->statistics_storage: %s\n" % e)

    print("----- statistics_task_by_metadata -----")
    try:
        # Get statistics about tasks executions, grouped by metadata
        api_response = api_instance.statistics_task_by_metadata()
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling StatisticsApi->statistics_task_by_metadata: %s\n" % e)

    print("----- statistics_task_by_status -----")
    try:
        # Get statistics about tasks executions, grouped by status
        api_response = api_instance.statistics_task_by_status()
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling StatisticsApi->statistics_task_by_status: %s\n" % e)

    print("----- statistics_task_by_storage -----")
    try:
        # Get statistics about tasks executions, grouped by source and destination
        api_response = api_instance.statistics_task_by_storage()
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling StatisticsApi->statistics_task_by_storage: %s\n" % e)

    print("----- statistics_task_by_workflow -----")
    try:
        # Get statistics about tasks executions, grouped by workflow
        api_response = api_instance.statistics_task_by_workflow()
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling StatisticsApi->statistics_task_by_workflow: %s\n" % e)