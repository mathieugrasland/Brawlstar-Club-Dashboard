from google.cloud import bigquery
from google.cloud import secretmanager
import json
import os

PROJECT_NUMBER = os.environ.get("PROJECT_NUMBER")

secrets = secretmanager.SecretManagerServiceClient()

bs_secrets = secrets.access_secret_version(request={"name": "projects/" + PROJECT_NUMBER + "/secrets/bs-dashboard-secrets/versions/latest"}).payload.data.decode("utf-8")
bs_secrets = json.loads(bs_secrets)

club_tag = bs_secrets['club_tag']
PROJECT_ID = bs_secrets['PROJECT_ID']
DATASET_ID = bs_secrets['DATASET_ID']
TABLE_ID = bs_secrets['TABLE_ID']


def main(request, context):

    client = bigquery.Client()

    # 1) create table
    schema = [
        bigquery.SchemaField("seasonday", "STRING", mode="REQUIRED"),
        bigquery.SchemaField("season", "STRING", mode="REQUIRED"),
        bigquery.SchemaField("day", "STRING", mode="REQUIRED"),
        bigquery.SchemaField("datetime", "DATETIME", mode="REQUIRED"),
        bigquery.SchemaField("timestamp", "STRING", mode="REQUIRED"),
        bigquery.SchemaField("name", "STRING", mode="REQUIRED"),
        bigquery.SchemaField("tag", "STRING", mode="REQUIRED"),
        bigquery.SchemaField("result", "STRING", mode="REQUIRED"),
        bigquery.SchemaField("mode", "STRING", mode="REQUIRED"),
        bigquery.SchemaField("brawler", "STRING", mode="REQUIRED"),
        bigquery.SchemaField("points", "INT64", mode="REQUIRED"),
        bigquery.SchemaField("used_tickets", "INT64", mode="REQUIRED"),
        bigquery.SchemaField("with_club_mate", "BOOLEAN", mode="REQUIRED")
    ]

    table = bigquery.Table(f"{PROJECT_ID}.{DATASET_ID}.{TABLE_ID}", schema=schema)
    table = client.create_table(table)
    return str(table)
