from pipelines.bronze import run_bronze
from pipelines.silver import run_silver
from pipelines.gold import run_gold
from pipelines.ml import train_model

if __name__ == "__main__":
    run_bronze()
    run_silver()
    run_gold()
    train_model()