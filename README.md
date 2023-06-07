# This project server as solution for assigment at O2

## Problem
We will use very simple problem in which we will try to predict a usefulness of reviews based review properties. We will use the data from yelp dataset.


## Approach
I first analalyzed the data in explore/exploration.ipynb notebook. I than used the gained knowledge
what data and how to extract them. I have decided to use pyspark for the whole pipeline, as it makes the whole process way faster. It looks very much like classic etl pipeilne, unlike the start
where I filter dataset (not your typical etl step). The filtering is done mostly to remove unwanted data, or to make the whole process faster. The pipeline
expects a json config like this:
```
{
  "output_path": "artifacts/feature_store",
  "data_path": "artifacts/data",
  "transform_path": "artifacts/transforms",
  "transform_tag": "v1",
  "filter_config":
    {
      "language": "en",
      "sample_rate": "1.0"
    },
  "split_config": {
    "train": 0.95,
    "test": 0.05
  },
  "tag": "yelp2020"
}
```

which specifies from where to load, where to save, how to filter and hot to tag the resulting data. The split config defines how and whether to split data into train and test. If we were doing inference we would not use filter_config and split_config.

The important property of pipeline is that we can later use same pipeline to transform the data for inference. We just need to use the same transform_tag. The pipeline will than load the transform from transform_path and apply it to the data.

## Decisions

### Data extraction
The whole project is using local filesystem, for everything. I have done so as it's really the fastest
way to setup stuff. I had more time, I would use proper feature store and likely auto download the dataset (both links I found requires login) thus simple `wget` wouldn't work.

#### Transformations in pipeline
We do the tf-idf transformation in pipeline. This now posses a problem,
that we somehow need to persist this transformation. We thus introduce
a version attribute, which is connected to that transformation. We clearly could do the transformation in the model and than ship it with it, but it's really slow and doing this on every model, would really slow done the whole ML process. The disadvantage is that, it's a bit harder to execute, as we need to keep track of the transforms (We need to transform the inference data in the same way as the training data).

## What's missing

Pipeline:
- tests/validation
- proper logging
- proper error handling
- proper documenation (mainly for features)

ML:
- proper hyperparameter tuning



## How to run
### Prerequisities
- python 3.10

### Installation
- `pip install -r requirements.txt`
- download data from https://www.yelp.com/dataset/download
- unzip it to `artifacts/data`

### Run ETL for transformation
- `bash run_pipeline.sh`
this will generate a report to reports, create transforms and save the data to artifacts/feature_store.

### Run training
For training I haven't made any script, because I was running it in jupyter notebooks. Both notebooks for hf and scikit are in `ml` folder.
Unfortunately I had some trubles with cuda drivers, so I couldn't fully train the bert model.
