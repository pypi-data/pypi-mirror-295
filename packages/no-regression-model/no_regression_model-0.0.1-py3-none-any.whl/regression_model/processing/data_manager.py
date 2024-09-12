import typing as t
from pathlib import Path

import joblib
import pandas as pd
from sklearn.pipeline import Pipeline

from regression_model import __version__ as _version
from regression_model.config.core import DATASET_DIR, TRAIN_MODEL_DIR, config

def load_dataset(*, filename: str) -> pd.DataFrame:
    dataframe = pd.read_csv(Path(f"{DATASET_DIR}/{filename}"))

    #rename variables begining with numbers to avoid syntax error later
    transformed = dataframe.rename(columns=config.model_conf.variables_to_rename)
    return transformed


def save_pipeline(*, pipeline_to_persist: Pipeline) -> None:
    """persist the pipeline,
    Saves the version models, and overwrite any previous 
    saved models. this ensures that when the package is
    published, there is only trained model that can be called,
    and we know exactly how it's built.
    """

    # prepare versioned save file name
    save_file_name = f"{config.app_config.pipeline_save_file}{_version}.pkl"
    save_path = TRAIN_MODEL_DIR / save_file_name

    remove_older_pipelines(files_to_keep=[save_file_name])
    joblib.dump(pipeline_to_persist, save_path)



def load_pipeline(*, file_name: str) -> Pipeline:
    "Load a persisted pipeline"
    file_path = TRAIN_MODEL_DIR / file_name
    trained_model = joblib.load(filename=file_path)
    return trained_model


def remove_older_pipelines(*, files_to_keep: t.List[str]) -> None:
    """
    Remove old model pipelines.
    This is to ensure there is a simple one-to-one
    mapping between the package version and the model
    version to be imported and used by other applications.
    """
    do_not_delete = files_to_keep + ["__init__.py"]
    for model_file in TRAIN_MODEL_DIR.iterdir():
        if model_file.name not in do_not_delete:
            model_file.unlink()


