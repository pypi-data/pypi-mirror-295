import requests
import json
from google.cloud import bigquery
from google.oauth2 import service_account
from googleapiclient.discovery import build
from databricks.sdk.runtime import *

def query_asana(query, asana_bearer_token):

    auth_header = "Bearer " + asana_bearer_token
    header = {"Authorization": auth_header}
    base_url = "https://app.asana.com/api/1.0"

    url = base_url + query
    response = requests.get(url, headers=header).json()
    result = response["data"]
    while response["next_page"]:
        next_page = response["next_page"]["uri"]
        response = requests.get(next_page, headers=header).json()
        result = result + response["data"]
    return json.dumps(result)


# COMMAND ----------


def query_everhour(query, everhour_api_key):
    # Everhour connection params
    base_url = "https://api.everhour.com"
    header = {"Content-Type": "application/json", "X-Api-Key": everhour_api_key}

    url = base_url + query

    try:
        response = requests.get(url, headers=header)

        # Log the HTTP status code
        print(f"HTTP Status Code: {response.status_code}")
        # Raise an HTTPError if the response code was not 2XX
        response.raise_for_status()

        return response.text
    except requests.exceptions.RequestException as e:
        # Log any exceptions
        print(f"API call failed: {e}")


# COMMAND ----------


def query_freshteams(query, freshteams_api_key):
    # Freshteams connection params
    base_url = "https://synaptiq.freshteam.com/api"
    header = {
        "accept": "application/json",
        "Authorization": "Bearer " + freshteams_api_key,
    }
    url = base_url + query

    result = requests.get(url, headers=header).text
    return result


# COMMAND ----------


# retrieve the token from the tmp file store in order to handle 60 day expiration and refresh
def read_xero_token():
    return dbutils.fs.head("/tmp/xero")


def write_xero_token(token):
    dbutils.fs.put("/tmp/xero", token, True)


def get_xero_access_token(xero_client_id, xero_client_secret):
    url = "https://identity.xero.com/connect/token"

    # boot strap with this then load from temp file
    # TODO: write back to secret or at least fall back to secret on failure/missing
    # refresh_token = dbutils.secrets.get(scope='synaptiq_dw', key='xero_refresh_token')
    refresh_token = read_xero_token()
    response = requests.post(
        url,
        headers={"Content-Type": "application/x-www-form-urlencoded"},
        data={
            "grant_type": "refresh_token",
            "client_id": xero_client_id,
            "client_secret": xero_client_secret,
            "refresh_token": refresh_token,
        },
    )
    json_response = response.json()
    write_xero_token(json_response["refresh_token"])
    return json_response["access_token"]


def query_xero(query, object_type, xero_tenant_id, xero_client_id, xero_client_secret):

    base_url = "https://api.xero.com/api.xro/2.0"
    header = {
        "Authorization": "Bearer "
        + get_xero_access_token(xero_client_id, xero_client_secret),
        "Accept": "application/json",
        "Xero-tenant-id": xero_tenant_id,
    }
    url = base_url + query
    response = requests.get(url, headers=header).json()
    return json.dumps(response[object_type])


# COMMAND ----------


def list_gsuite_users(credentials_json, subject=None):
    credentials_dict = json.loads(credentials_json)
    creds = service_account.Credentials.from_service_account_info(
        credentials_dict,
        scopes=["https://www.googleapis.com/auth/admin.directory.user.readonly"],
        subject=subject,
    )

    # Build the API service
    service = build("admin", "directory_v1", credentials=creds)

    # Call the API to list all users
    users = service.users().list(customer="C01gp0xmn").execute()
    return json.dumps(users.get("users", []))


# COMMAND ----------


def write_data_to_delta(spark, data, table_name, database_name):
    destination = database_name + "." + table_name
    # escape out any key names with disallowed characters
    cleaned_data = escape_keys(json.loads(data))
    # find the python incantation to delete or merge the table first
    spark.read.json(sc.parallelize([json.dumps(cleaned_data)])).write.mode(
        "overwrite"
    ).option("overwriteSchema", "true").format("delta").saveAsTable(destination)


def write_df_to_delta(spark, data_frame, table_name, write_to_bigquery, database_name):
    spark_df = spark.createDataFrame(data_frame)
    spark_df.write.mode("overwrite").option("overwriteSchema", "true").saveAsTable(
        database_name + "." + table_name
    )
    if write_to_bigquery:
        write_df_to_bigquery(data_frame, table_name)


def write_df_to_bigquery(df, table_name, bq_client):
    file_path = "/tmp/" + table_name + ".csv"
    df.to_csv(file_path, index=False)
    table_id = "synaptiq_data_warehouse." + table_name
    print("about to create table: " + table_id + " in BigQuery")

    job_config = bigquery.LoadJobConfig(
        source_format=bigquery.SourceFormat.CSV,
        skip_leading_rows=1,
        autodetect=True,
        allow_quoted_newlines=True,
        write_disposition="WRITE_TRUNCATE",
    )

    with open(file_path, "rb") as source_file:
        job = bq_client.load_table_from_file(
            source_file, table_id, job_config=job_config
        )

    job.result()  # Waits for the job to complete.

    table = bq_client.get_table(table_id)  # Make an API request.
    print(
        "Loaded {} rows and {} columns to {}".format(
            table.num_rows, len(table.schema), table_id
        )
    )


def save_output(data, table_name):
    dbutils.fs.put("/FileStore/" + table_name + ".json", data, True)


# find and replace all key names with a new key name
def escape_keys(data, characters=[" ", ",", ";", "{", "}", "(", ")", "\n", "\t", "="]):
    if isinstance(data, list):
        for item in data:
            escape_keys(item, characters)
    elif isinstance(data, dict):
        for key, value in list(data.items()):
            new_key = key
            for char in characters:
                if new_key.find(char) != -1:
                    new_key = new_key.replace(char, "_")
            data[new_key] = data.pop(key)
            escape_keys(value, characters)
    return data
