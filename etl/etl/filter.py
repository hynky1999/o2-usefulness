from etl import FilterConfig, ETLConfig
from ftlangdetect import detect
from pyspark.sql import DataFrame
from pyspark.sql.functions import udf
from pyspark.sql.types import StringType

def sample_reviews(df: DataFrame , sample_rate: float):
    return df.sample(False, sample_rate, 42)

def detect_all_lines_lang(text):
    return detect(" ".join(text.split("\n")))["lang"]

def filter_on_language(df: DataFrame, language: str):
    udf_detect = udf(detect_all_lines_lang, StringType())
    df = df.withColumn("lang", udf_detect("text"))
    df = df.filter(df["lang"] == language)
    df = df.drop("lang")
    return df

def filter_reviews(config: ETLConfig, dfs: dict[str, DataFrame]):
    reviews_df = dfs["reviews"]
    # Sample first to reduce the size of the dataset
    reviews_df = sample_reviews(reviews_df, config.filter_config.sample_rate)
    reviews_df = filter_on_language(reviews_df, config.filter_config.language)
    return { "reviews": reviews_df, "users": dfs["users"] }

def filter(config: ETLConfig, dfs: dict[str, DataFrame]):
    if config.filter_config is not None:
        dfs = filter_reviews(config, dfs)
    return dfs



    



    
    
