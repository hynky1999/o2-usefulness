import argparse
import logging
from pyspark.sql import SparkSession
from etl import ETLConfig
from etl.etl import etl_extract, etl_filter, etl_load, etl_transform, etl_split, get_storage_path


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--config', type=str, default='config.yaml')
    return parser.parse_args()

def init_spark():
    # In non-assigment code, we would init based on dotenv
    return SparkSession.builder.master("local[*]").appName("etl").config("spark.executor.memory", "32g").config("spark.driver.memory", "32g").config("spark.driver.maxResultSize", "32g").getOrCreate()

def run_pipe(config: ETLConfig, spark: SparkSession):
    dfs = etl_extract(config, spark)
    dfs_splits = etl_split(config, dfs)
    for split, dfs in dfs_splits:
        logging.info(f"Processing split {split}")
        dfs = etl_filter(config, dfs)
        df = etl_transform(config, dfs)
        etl_load(config, df, split)
        logging.info(f"Finished processing split {split}")


def run():
    args = get_args()
    # load from json
    config = ETLConfig.parse_file(args.config)
    # Early validation
    if get_storage_path(config).exists():
        raise Exception("Tag already exists")

    spark = init_spark()
    run_pipe(config, spark)


if __name__ == "__main__":
    run()