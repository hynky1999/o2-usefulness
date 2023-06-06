from pathlib import Path
from pyspark.sql import SparkSession
from etl import ETLConfig

def extract_from_storage(path: Path, spark: SparkSession):
    reviews_df = spark.read.json(str(path / "yelp_academic_dataset_review.json"))
    users_df = spark.read.json(str(path / "yelp_academic_dataset_user.json"))
    reviews_df = reviews_df.withColumnRenamed("useful", "useful_votes")

    return { "reviews": reviews_df, "users": users_df }


def extract(config: ETLConfig, spark: SparkSession):
    """
    Normally we would use a cloud storage like S3 or GCS, but
    for simplicity we will use the local filesystem
    """

    return extract_from_storage(config.data_path, spark)