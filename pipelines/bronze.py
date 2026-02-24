from utils.bq_client import get_bq_client, get_config

def run_bronze():
    config = get_config()
    client = get_bq_client()

    query = f"""
    CREATE OR REPLACE TABLE `{config['project_id']}.{config['dataset_id']}.bronze_orders` AS
    SELECT * FROM `bigquery-public-data.thelook_ecommerce.orders`
    """

    client.query(query).result()
    print("✅ Bronze Layer Created")