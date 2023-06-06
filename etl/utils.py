from pydantic import BaseModel
from dataclasses import dataclass
from pathlib import Path
from pyspark.ml.feature import ImputerModel, IDFModel
import uuid

class FilterConfig(BaseModel):
    """Config class for filtering"""
    sample_rate: float
    language: str

@dataclass
class Transforms:
    """Config class for transforms"""
    idfModel: IDFModel | None = None
    imputer: ImputerModel | None = None


class Splits(BaseModel):
    train: float
    test: float

class TFIDFConfig(BaseModel):
    """Config class for TFIDF"""
    min_df: int = 0


class ETLConfig(BaseModel):
    """Config class for ETL

    Attributes:
        data_path: Path to data directory
        output_path: Path to output directory
        transform_version: Version of transform if None train new transforms
    """
    output_path: Path
    data_path: Path
    transform_path: Path | None
    transform_tag: str | None
    filter_config: FilterConfig | None
    splits_config: Splits | None
    tfidf_config: TFIDFConfig = TFIDFConfig()
    tag: str

    # Generate a tag if not provided
    def generate_tag(self):
        return str(uuid.uuid4())

    def __post_init__(self):
        if self.tag is None:
            self.tag = self.generate_tag()
