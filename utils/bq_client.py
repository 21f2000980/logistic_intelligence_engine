from google.cloud import bigquery
import yaml

def get_config():
    with open("config/config.yaml") as f:
        return yaml.safe_load(f)

def get_bq_client():
    config = get_config()
    return bigquery.Client(project=config["project_id"])