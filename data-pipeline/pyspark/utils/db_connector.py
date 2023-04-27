import os
from influxdb_client import InfluxDBClient

__db_uri = os.getenv("DB_URI")
if __db_uri is None:
    raise RuntimeError("DB_URI is not defined in runtime environment")

db_org = os.getenv("INFLUXDB_ORG")
if db_org is None:
    raise RuntimeError("INFLUXDB_ORG is not defined in runtime environment")

db_bucket = os.getenv("INFLUXDB_BUCKET")
if db_bucket is None:
    raise RuntimeError("INFLUXDB_BUCKET is not defined in runtime environment")

__token = os.getenv("INFLUXDB_ADMIN_TOKEN")
if __token is None:
    raise RuntimeError("INFLUXDB_ADMIN_TOKEN is not defined in runtime environment")

__db_user = os.getenv("INFLUXDB_USERNAME")
if __db_user is None:
    raise RuntimeError("INFLUXDB_USERNAME is not defined in runtime environment")

__db_pass = os.getenv("INFLUXDB_PASSWORD")
if __db_pass is None:
    raise RuntimeError("INFLUXDB_PASSWORD is not defined in runtime environment")

db_client = InfluxDBClient(
    url=__db_uri, org=db_org, token=__token, username=__db_user, password=__db_pass
)
