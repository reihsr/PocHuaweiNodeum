from __future__ import print_function
import time
import nodeum_sdk
from nodeum_sdk.rest import ApiException
from pprint import pprint
from jproperties import Properties

configs = Properties()
with open('config.properties', 'rb') as config_file:
    configs.load(config_file)
configuration = nodeum_sdk.Configuration()

# Configure HTTP basic authorization: BasicAuth
configuration.username = configs.get("NODEUM_User").data
configuration.password = configs.get("NODEUM_PWD").data
#configuration = nodeum_sdk.Configuration()
# Configure API key authorization: BearerAuth
#configuration.api_key['Authorization'] = '9Duke5xqeuS0CWTBzuS6hA'#'YOUR_API_KEY'

# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
#configuration.api_key_prefix['Authorization'] = 'Bearer'

# Defining host is optional and default to http://localhost/api/v2
configuration.host = "http://" + configs.get("NODEUM_HOST").data + "/api/v2"

# Defining host is optional and default to http://localhost/api/v2
configuration.host = "http://" + configs.get("NODEUM_HOST").data + "/api/v2"
# Enter a context with an instance of the API client
with nodeum_sdk.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = nodeum_sdk.CloudBucketsApi(api_client)
    limit = 56 # int | The number of items to display for pagination. (optional)
offset = 56 # int | The number of items to skip for pagination. (optional)
sort_by = ['sort_by_example'] # list[str] | Sort results by attribute.  Can sort on multiple attributes, separated by `|`. Order direction can be suffixing the attribute by either `:asc` (default) or `:desc`. (optional)
id = 'id_example' # str | Filter on id (optional)
cloud_connector_id = 'cloud_connector_id_example' # str | Filter on cloud connector id (optional)
pool_id = 'pool_id_example' # str | Filter on a pool id (optional)
name = 'name_example' # str | Filter on name (optional)
location = 'location_example' # str | Filter on location (optional)
price = 'price_example' # str | Filter on price (optional)

try:
        # Lists all cloud buckets.
        api_response = api_instance.index_cloud_buckets(limit=limit, offset=offset, sort_by=sort_by, id=id, cloud_connector_id=cloud_connector_id, pool_id=pool_id, name=name, location=location, price=price)
        pprint(api_response)
except ApiException as e:
        pprint("Exception when calling CloudBucketsApi->index_cloud_buckets: %s\n" % e)