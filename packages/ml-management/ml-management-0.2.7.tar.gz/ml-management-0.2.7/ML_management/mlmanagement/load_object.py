import os.path
import subprocess
import sys
import traceback
from typing import Optional

import mlflow
from ML_management import mlmanagement
from ML_management.mlmanagement.model_type import ModelType


def _load_model_type(
    name: str,
    version: int,
    model_type: ModelType,
    unwrap: bool = True,
    install_requirements: bool = False,
    dst_path: Optional[str] = None,
):
    """Load model from local path."""
    local_path = mlmanagement.MlflowClient().download_artifacts_by_name_version(
        name=name, version=version, model_type=model_type, path="", dst_path=dst_path
    )
    if install_requirements:
        _set_model_version_requirements(local_path)
    loaded_model = mlflow.pyfunc.load_model(model_uri=local_path, suppress_warnings=True)
    if unwrap:
        artifacts_path = loaded_model._model_impl.context._artifacts
        loaded_model = loaded_model.unwrap_python_model()
        loaded_model.artifacts = artifacts_path
    return loaded_model


def load_dataset(
    name: str, version: int, install_requirements: bool = False, unwrap: bool = True, dst_path: Optional[str] = None
):
    """Download all model's files for loading model locally.

    Parameters
    ==========
    name: str
        Name of the dataset.
    version: int
        Version of the dataset.
    install_requirements: bool = False
        Whether to install dataset requirements. Default: False.
    unwrap: bool = True
        Whether to unwrap dataset. Default: True.
    dst_path: Optional[str]: None
        Destination path. Default: None.
    Returns
    =======
    DatasetLoaderPattern
        The object of the dataset to use.
    """
    return _load_model_type(name, version, ModelType.DATASET_LOADER, unwrap, install_requirements, dst_path)


def _set_model_version_requirements(local_path) -> None:
    """Installing requirements of the model locally."""
    with open(os.path.join(local_path, "requirements.txt")) as req:
        requirements = req.read().split("\n")
    try:
        subprocess.check_call(
            [sys.executable, "-m", "pip", "install", "--no-cache-dir", "--default-timeout=100", *requirements]
        )
    except Exception:
        print(traceback.format_exc())


def load_model(
    name: str, version: int, install_requirements: bool = False, unwrap: bool = True, dst_path: Optional[str] = None
):
    """Download all model's files for loading model locally.

    Parameters
    ==========
    name: str
        Name of the model.
    version: int
        Version of the model.
    install_requirements: bool = False
        Whether to install model requirements. Default: False.
    unwrap: bool = True
        Whether to unwrap model. Default: True.
    dst_path: Optional[str]: None
        Destination path. Default: None.
    Returns
    =======
    Model
        The object of the model to use.
    """
    return _load_model_type(name, version, ModelType.MODEL, unwrap, install_requirements, dst_path)


def load_executor(
    name: str, version: int, install_requirements: bool = False, unwrap: bool = True, dst_path: Optional[str] = None
):
    """Download all model's files for loading model locally.

    Parameters
    ==========
    name: str
        Name of the executor.
    version: int
        Version of the executor.
    install_requirements: bool = False
        Whether to install executor requirements. Default: False.
    unwrap: bool = True
        Whether to unwrap executor. Default: True.
    dst_path: Optional[str]: None
        Destination path. Default: None.
    Returns
    =======
    BaseExecutor
        The object of the executor to use.
    """
    return _load_model_type(name, version, ModelType.EXECUTOR, unwrap, install_requirements, dst_path)
