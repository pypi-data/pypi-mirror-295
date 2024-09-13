import pathlib
import site
from pprint import pprint
import sys

site.addsitedir("../src")

from pingintel_api import PingMapsAPIClient
from pingintel_api.pingmaps import types as t
from pingintel_api import SOVFixerAPIClient

SCRIPT_DIR = pathlib.Path(__file__).parent

api_client = PingMapsAPIClient(environment="local", api_url="http://127.0.0.1")
# api_client = PingMapsAPIClient(environment="dev2")
# sovfixer_api = SOVFixerAPIClient(environment="dev2")

sovid = "s-ga-ping-6zmxh4"
sovid = "s-lo-ping-y7qzns"
# sovid = "s-lo-ping-eajee"
# sovid = sovfixer_api.list_activity(page_size=1)["results"][0]["id"]

filter_params: t.PingMapsPolicyLocationRequest = {
    "sovid": sovid,
    "lat1": 30.0583,
    "lng1": -64.4057,
    "lat2": 40.7128,
    "lng2": -74.0060,
    "limit": 3,
    # "const__code_air": 301,
    "show_points_sooner": False,
}

breakdowns = api_client.get_policy_breakdown(
    sovid=sovid, fields=["const__bldg_year_built__bins"], limit=2
)
pprint(breakdowns)

# breakdowns = api_client.get_policy_breakdown(
#     sovid=sovid,
#     fields=["const__bldg_year_built__bins"],
#     const__bldg_year_built__gte=1978,
# )
# pprint(breakdowns)

# breakdowns = api_client.get_policy_breakdown(
#     sovid=sovid,
#     fields=["const__bldg_year_built__bins"],
#     const__bldg_year_built__bins=["1970 - 1979", "1990 - 1999"],
#     limits__total_limit__lte=1000000,
#     limits__total_limit__gte=1000,
#     attach=50,
#     layer_limit=90,
# )
# pprint(breakdowns)

# breakdowns = api_client.get_policy_breakdown(
#     sovid=sovid,
#     fields=["const__bldg_year_built__bins"],
#     const__bldg_year_built__bins=["1970 - 1979", "1990 - 1999"],
# )

# breakdowns = api_client.get_policy_breakdown(**filter_params)
# pprint(breakdowns)

activity_results = api_client.get_policy_locations(
    sovid=sovid, **breakdowns["totals"]["bbox"], limit=1
)
pprint(activity_results)

activity_results = api_client.get_policy_locations(
    sovid=sovid, **breakdowns["totals"]["bbox"], limit=10000
)
pprint(activity_results)

# print("with filters!!!")
# breakdowns = api_client.get_policy_breakdown(**filter_params)
# pprint(breakdowns)
# activity_results = api_client.get_policy_locations(**filter_params)
# pprint(activity_results)
