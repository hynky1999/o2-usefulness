from pathlib import Path
from pyspark.sql import DataFrame
from etl import ETLConfig


def split(config: ETLConfig, dfs: dict[str, DataFrame]):
    """
    Split the data into train, test if splits_config is provided

    Returns:
        List[Tuple[str, DataFrame]]: Ordered list of splits
    """

    reviews_df = dfs["reviews"]
    # split the data into train, test,
    splits = [("general", reviews_df)]
    if config.splits_config is not None:
        train_df, test_df = reviews_df.randomSplit([config.splits_config.train, config.splits_config.test], seed=42)
        splits = [("train", train_df), ("test", test_df)]

    return [(name, {"reviews": df, "users": dfs["users"]}) for name, df in splits]


 



    

