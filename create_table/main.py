from google.cloud import bigquery
from google.cloud import secretmanager

# TODO get secrets
PROJECT_ID = "bs-club-dash"
DATASET_ID = "club_logs"
TABLE_ID = "battle_logs"


def main(request, context):

    client = bigquery.Client()

    # 1) create table
    schema = [
        bigquery.SchemaField("name", "STRING", mode="REQUIRED"),
        bigquery.SchemaField("tag", "STRING", mode="REQUIRED"),
        bigquery.SchemaField("points", "INT64", mode="REQUIRED"),
        bigquery.SchemaField("result", "STRING", mode="REQUIRED"),
        bigquery.SchemaField("mode", "STRING", mode="REQUIRED"),
        bigquery.SchemaField("timestamp", "STRING", mode="REQUIRED"),
        bigquery.SchemaField("used_tickets", "INT64", mode="REQUIRED")
    ]

    table = bigquery.Table(f"{PROJECT_ID}.{DATASET_ID}.{TABLE_ID}", schema=schema)
    table = client.create_table(table)
    return str(table)