from dataclasses import dataclass
from typing import List
from sklearn.metrics import confusion_matrix, f1_score
import seaborn as sns
import wandb
import numpy as np
import pickle
from pathlib import Path

@dataclass
class Result:
    metric_name: str
    metric_value: float

CUR_DIR = Path(__file__).parent


def get_model_folder():
    return CUR_DIR / "models" / wandb.run.id

def create_confusion_matrix(true: np.ndarray, predicted: np.ndarray, labels: List[str], ax):
    conf = confusion_matrix(true, predicted, labels=labels, normalize="pred")
    sns.heatmap(conf, annot=True, ax=ax, cmap="Blues", fmt=".2f")
    ax.set_xticklabels(labels)
    ax.set_yticklabels(labels)
    ax.set_title("Confusion Matrix")
    ax.set_xlabel("Predicted Labels")
    ax.set_ylabel("True Labels")
    return ax


def get_result(true: np.ndarray, predicted: np.ndarray):
    #  We use f1_macro as our metric
    return Result("f1_macro", f1_score(true, predicted, average="macro"))

def get_cv_metric():
    return "f1_macro"


def save_model(model):
    path = get_model_folder() / "model.pkl"
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "wb") as f:
        pickle.dump(model, f)
    return path

def save_experiment(model, result: Result):
    wandb.log({result.metric_name: result.metric_value})
    path = save_model(model)
    artifact = wandb.Artifact("model", type="model", description="model trained on o2 dataset")
    artifact.add_file(path)
    wandb.log_artifact(artifact)
    wandb.finish()

def init_experiment(cfg):
    wandb.init(project="o2", config=cfg)
