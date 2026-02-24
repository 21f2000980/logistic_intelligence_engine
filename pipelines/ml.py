from utils.bq_client import get_bq_client, get_config

def train_model():
    config = get_config()
    client = get_bq_client()

    query = f"""
    CREATE OR REPLACE MODEL `{config['project_id']}.{config['dataset_id']}.delay_predictor`
    OPTIONS(model_type='linear_reg', input_label_cols=['avg_delay']) AS
    SELECT order_date, avg_delay
    FROM `{config['project_id']}.{config['dataset_id']}.gold_logistics_master`
    """

    client.query(query).result()
    print("✅ ML Model Trained")