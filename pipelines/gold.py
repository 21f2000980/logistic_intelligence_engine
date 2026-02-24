from utils.bq_client import get_bq_client, get_config

def run_gold():
    config = get_config()
    client = get_bq_client()

    query = f"""
    CREATE OR REPLACE TABLE `{config['project_id']}.{config['dataset_id']}.gold_logistics_master`
    PARTITION BY order_date AS
    SELECT
      order_date,
      COUNT(*) AS total_orders,
      AVG(delay_days) AS avg_delay
    FROM `{config['project_id']}.{config['dataset_id']}.silver_orders`
    GROUP BY order_date
    """

    client.query(query).result()
    print("✅ Gold Layer Created")