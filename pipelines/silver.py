from utils.bq_client import get_bq_client, get_config

def run_silver():
    config = get_config()
    client = get_bq_client()

    query = f"""
    CREATE OR REPLACE TABLE `{config['project_id']}.{config['dataset_id']}.silver_orders` AS
    SELECT
      *,
      DATE(created_at) AS order_date,
      TIMESTAMP_DIFF(shipped_at, created_at, DAY) AS delay_days
    FROM `{config['project_id']}.{config['dataset_id']}.bronze_orders`
    WHERE status = 'Complete'
    """

    client.query(query).result()
    print("✅ Silver Layer Created")