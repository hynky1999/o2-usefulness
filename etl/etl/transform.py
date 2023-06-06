from typing import Any
from etl import ETLConfig, Transforms, TFIDFConfig
from pyspark.sql import DataFrame
import pyspark.sql.functions as F
from pyspark.ml.feature import Tokenizer, IDF, HashingTF, Imputer, IDFModel, ImputerModel
import logging

IMPUTED_COLS = [
    # Reviews
    "stars",
    # Users
    "user_age", "user_review_count", "user_cool", "user_funny", "user_fans", "user_average_stars", "user_compliment_cool", "user_compliment_cute", "user_compliment_list"
]



def add_user_features(df: DataFrame):
    # Placeholder to get positive values
    since = 1970
    # Should be at least 0
    df = df.withColumn("user_age", F.year(F.col("user_yelping_since")) - since)
    return df

def categorize_usefulness(df: DataFrame):
    df = df.withColumn("usefulness", F.when(F.col("useful_votes") <= 1, "Not useful").
                                               otherwise(F.when(F.col("useful_votes") >= 5, "Very useful").
                                               otherwise("Useful")))
    return df


def add_tfidf(df: DataFrame, transforms: Transforms, config: TFIDFConfig):
    tokenizer = Tokenizer(inputCol="text", outputCol="words")
    hashingTF = HashingTF(inputCol="words", outputCol="idf_features")
    tokenized = tokenizer.transform(df)
    hashed = hashingTF.transform(tokenized).cache()
    if transforms.idfModel is None:
        idf = IDF(inputCol="idf_features", outputCol="text_tfidf",
                    minDocFreq=config.min_df)
        logging.info("Fitting IDF model")
        transforms.idfModel = idf.fit(hashed)
    
    tfidf = transforms.idfModel.transform(hashed)
    return tfidf


def add_text_properties(df: DataFrame):
    df = df.withColumn("text_length", F.length(df["text"]))
    df = df.withColumn("text_words", F.size(F.split(df["text"], " ")))
    return df

def enhance(df: DataFrame, transforms: Transforms, tfidf_config: TFIDFConfig):
    df = add_user_features(df)
    df = add_text_properties(df)
    df = add_tfidf(df, transforms, tfidf_config)
    df = categorize_usefulness(df)
    return df
    

def cast(df: DataFrame):
    df = df.withColumn("stars", F.col("stars").cast("int"))
    return df


def pre_transform(dfs: dict[str, DataFrame]):
    users_df = dfs["users"]
    users_df = users_df.select("user_id", "review_count", "useful", "funny", "cool", "yelping_since", "elite", "fans", "average_stars", "compliment_cool", "compliment_cute", "compliment_list")
    users_df.withColumn("yelping_since", F.to_date(users_df["yelping_since"]))
    # rename all columns to user_*
    users_df = users_df.select([F.col(col).alias(f"user_{col}") for col in users_df.columns if col != "user_id"] + ["user_id"])
    reviews_df = dfs["reviews"]
    reviews_df = reviews_df.select("user_id", "stars", "useful_votes", "text", "date", "review_id")
    reviews_df = reviews_df.withColumn("date", F.to_date(reviews_df["date"]))
    # use left join to keep all reviews
    joined = reviews_df.join(users_df, on="user_id", how="left")
    return joined

def impute(df: DataFrame, transforms: Transforms):
    if transforms.imputer is None:
        imputer = Imputer(inputCols=IMPUTED_COLS, outputCols=IMPUTED_COLS, strategy="mean")
        logging.info("Fitting imputer")
        transforms.imputer = imputer.fit(df)
    
    imputed = transforms.imputer.transform(df)
    return imputed


def get_transform_name(transform: str):
    return f"{transform}.model"

def get_transforms_path(config: ETLConfig):
    if config.transform_path is None or config.transform_tag is None:
        return None
    return config.transform_path / config.transform_tag

def load_transforms(config: ETLConfig):
    transforms = Transforms()
    transforms_path = get_transforms_path(config)

    # Load transforms if they exist
    if transforms_path is not None and transforms_path.exists():
        transforms = Transforms(
            idfModel=IDFModel(),
            imputer=ImputerModel()
        )
        for transform in transforms.__dict__:
            transforms.__dict__[transform] = transforms.__getattribute__(transform).load(str(transforms_path / get_transform_name(transform)))
        logging.info(f"Loaded pretrained transforms with tag {config.transform_tag}")
    return transforms


def save_transforms(config: ETLConfig, transforms: Transforms):
    path = get_transforms_path(config)
    if path is None:
        raise ValueError("Cannot save transforms, path is None or already exists")

    if path.exists():
        return path

    path.mkdir(parents=True)
    for transform in transforms.__dict__:
        transforms.__dict__[transform].save(str(path / get_transform_name(transform)))
    
    return path

def select_features(df: DataFrame):
    """
    This would likely service as descriptor for the data, if we had proper feature store
    
    """
    # Keep review id if we need to return data
    return df.select(
        IMPUTED_COLS + ["usefulness"] + ["text_length", "text_words", "text_tfidf", "text"]
        + ["review_id"]
    )
        

        

def transform(config: ETLConfig, dfs: dict[str, DataFrame]):
    transforms = load_transforms(config)
    transformed = pre_transform(dfs)
    enhanced = enhance(transformed, transforms, config.tfidf_config)
    casted = cast(enhanced)
    imputed = impute(casted, transforms)
    selected = select_features(imputed)

    # We will not normalize the data, this is simple and not costy, so can be done in the model
    # If we have transform_tag, we will save the transforms
    save_transforms(config, transforms)
    return selected



