from pathlib import Path
from pyspark.sql import DataFrame
from etl import ETLConfig

def load_to_storage(df: DataFrame, path: Path):
    # Normally we would push to a feature store or cloud storage
    # but for simplicity we will use the local filesystem
    df.write.parquet(str(path))

def get_storage_path(config: ETLConfig):
    return  config.output_path / config.tag

def load(config: ETLConfig, df: DataFrame, split: str):
    load_to_storage(df, get_storage_path(config) / split)