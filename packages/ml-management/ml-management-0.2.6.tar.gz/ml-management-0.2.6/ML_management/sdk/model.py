from typing import Optional

import pandas as pd
from sgqlc.operation import Operation

from ML_management.sdk import schema
from ML_management.sdk.schema import Model, ModelVersion
from ML_management.sdk.sdk import _to_datetime, send_graphql_request


def list_model() -> pd.DataFrame:
    """
    List available models.

    Returns
    -------
    pd.DataFrame
        Pandas dataframe with list of available models.
    """
    op = Operation(schema.Query)
    op.list_model.name()
    op.list_model.description()
    op.list_model.creation_timestamp()
    op.list_model.last_updated_timestamp()
    json_data = send_graphql_request(op)
    df = pd.DataFrame.from_dict(json_data["listModel"])
    if not df.empty:
        df = _to_datetime(df, ["creationTimestamp", "lastUpdatedTimestamp"])
    return df


def delete_model(model_name: str) -> bool:
    """
    Delete model and all of it's versions.

    Parameters
    ----------
    model_name: str
        Name of the model to delete.
    """
    op = Operation(schema.Mutation)
    op.delete_model(name=model_name)
    return send_graphql_request(op)["deleteModel"]


def set_model_tag(name: str, key: str, value: str) -> Model:
    """
    Set model tag.

    Parameters
    ----------
    name: str
        Name of the model.
    key: str
        Key tag.
    value: str
        Value tag.

    Returns
    -------
    Model
        Model instance with meta information.
    """
    op = Operation(schema.Mutation)
    set_tag = op.set_model_tag(name=name, key=key, value=value)
    set_tag.name()
    set_tag.tags()
    model = send_graphql_request(op=op)
    return Model(model)


def delete_model_tag(name: str, key: str) -> Model:
    """
    Delete model tag.

    Parameters
    ----------
    name: str
        Name of the model.
    key: str
        Key tag.

    Returns
    -------
    Model
        Model instance with meta information.
    """
    op = Operation(schema.Mutation)
    delete_tag = op.delete_model_tag(name=name, key=key)
    delete_tag.name()
    delete_tag.tags()
    model = send_graphql_request(op=op)
    return Model(model)


def set_model_description(name: str, description: str) -> Model:
    """
    Set model description.

    Parameters
    ----------
    name: str
        Name of the model.
    description: str
        Description model.

    Returns
    -------
    Model
        Model instance with meta information.
    """
    op = Operation(schema.Mutation)
    set_description = op.set_model_description(name=name, description=description)
    set_description.name()
    set_description.description()

    model = send_graphql_request(op=op)
    return Model(model)


def list_model_version(name: str) -> pd.DataFrame:
    """
    List available versions of the model with such name.

    Parameters
    ----------
    name: str
        Name of the model.

    Returns
    -------
    pd.DataFrame
        Pandas dataframe with a list of available model versions.
    """
    op = Operation(schema.Query)
    base_query = op.model_from_name(name=name).list_model_version
    base_query.version()
    base_query.creation_timestamp()
    base_query.name()
    json_data = send_graphql_request(op)

    df = pd.DataFrame.from_dict(json_data["modelFromName"]["listModelVersion"])
    df = _to_datetime(df, ["creationTimestamp"])

    return df.sort_values(by=["version"], ignore_index=True)


def model_version_metainfo(name: str, version: Optional[int] = None) -> ModelVersion:
    """
    Meta information about the model version by the model name and version.

    Parameters
    ----------
    name: str
        Name of the model.
    version: Optional[int] = None
        Version of the model. Default: None, "latest" version is used.

    Returns
    -------
    ModelVersion
        ModelVersion instance with meta information.
    """
    op = Operation(schema.Query)
    _model_version = schema.ObjectVersionOptionalInput(name=name, version=version)
    base_query = op.model_version_from_name_version(model_version=_model_version)
    base_query.name()
    base_query.tags()
    base_query.run.run_id()
    base_query.version()
    base_query.build_job().status()
    base_query.build_job().build_object_name()
    base_query.available_executor_versions.name()
    base_query.available_executor_versions.version()
    model_version = send_graphql_request(op, json_response=False)
    return model_version.model_version_from_name_version


def rebuild_model_version_image(name: str, version: int) -> str:
    """
    Start building new docker image for specified model version.

    Parameters
    ----------
    name: str
        Name of the model.
    version: int
        Version of the model

    Returns
    -------
    str
        name of new docker image for specified model version.
    """
    op = Operation(schema.Mutation)
    _model_version = schema.ObjectVersionInput(name=name, version=version)
    op.rebuild_model_version_image(model_version=_model_version)
    result = send_graphql_request(op=op)
    return result["rebuildModelVersionImage"]


def cancel_venv_build_job_for_model_version(model_name: str, model_version: int) -> bool:
    """
    Cancel running or planned build job of model's environment.

    Parameters
    ----------
    model_name: str
        The name of the model.
    model_version: int
        The version of the model.
    """
    op = Operation(schema.Mutation)
    op.cancel_venv_build_job_for_model_version(name=model_name, version=model_version)
    return send_graphql_request(op)["cancelVenvBuildJobForModelVersion"]


def cancel_build_job_for_model_version(model_name: str, model_version: int) -> bool:
    """
    Cancel running or planned build job of model image.

    Parameters
    ----------
    model_name: str
        The name of the model.
    model_version: int
        The version of the model.
    """
    op = Operation(schema.Mutation)
    op.cancel_build_job_for_model_version(name=model_name, version=model_version)
    return send_graphql_request(op)["cancelBuildJobForModelVersion"]


def delete_model_version(model_name: str, model_version: int) -> bool:
    """
    Delete version of a model.

    Parameters
    ----------
    model_name: str
        The name of the model.
    model_version: int
        The version of the model.
    """
    op = Operation(schema.Mutation)
    op = Operation(schema.Mutation)
    model_version_choice = schema.ObjectVersionInput(name=model_name, version=model_version)
    op.delete_model_version_from_name_version(model_version=model_version_choice)
    return send_graphql_request(op)["deleteModelVersionFromNameVersion"]


def get_latest_model_version(name) -> ModelVersion:
    op = Operation(schema.Query)
    version = op.model_from_name(name=name).latest_model_version()
    version.name()
    version.version()
    version.tags()
    version.description()
    version.run.run_id()
    model_version = send_graphql_request(op)["modelFromName"]["latestModelVersion"]
    return ModelVersion(model_version)


def get_initial_model_version(name) -> ModelVersion:
    op = Operation(schema.Query)
    version = op.model_from_name(name=name).init_model_version()
    version.name()
    version.version()
    version.tags()
    version.description()
    version.run.run_id()
    model_version = send_graphql_request(op)["modelFromName"]["initModelVersion"]
    return ModelVersion(model_version)


def serve_model(name: str, version: Optional[int] = None, gpu: bool = False) -> str:
    """
    Start model serving in triton service.

    Parameters
    ----------
    name: str
        Name of the model.
    version: Optional[int] = None
        Version of the model. Default: None, "latest" version is used.
    gpu: bool
        Determine which device will be used: GPU or CPU. Default: False, CPU is used.

    Returns
    -------
    str:
        endpoint path to make inference requests for model version.
    """
    if version is None:
        version = get_latest_model_version(name).version

    op = Operation(schema.Mutation)
    serving_parameters = schema.ModelServingInput(
        model_version=schema.ObjectVersionInput(name=name, version=version), gpu=gpu
    )
    op.serve_model(serving_parameters=serving_parameters)
    send_graphql_request(op)
    return f"/v2/models/{name}/versions/{version}/infer"


def stop_model_serving(name: str, version: Optional[int] = None) -> None:
    """
    Stop model serving in triton service.

    Parameters
    ----------
    name: str
        Name of the model.
    version: Optional[int] = None
        Version of the model. Default: None, "latest" version is used.
    """
    if version is None:
        version = get_latest_model_version(name).version

    op = Operation(schema.Mutation)
    op.stop_model_serving(model_version=schema.ObjectVersionInput(name=name, version=version))
    send_graphql_request(op=op)
    print("Serving has been successfully stopped.")


def check_inference_model_readiness(name: str, version: Optional[int] = None) -> Optional[str]:
    """
    Check is model ready to accept requests.

    Parameters
    ----------
    name: str
        Name of the model.
    version: Optional[int] = None
        Version of the model. Default: None, "latest" version is used.

    Returns
    -------
    Optional[str]:
        endpoint path to make requests if model is ready else None
    """
    if version is None:
        version = get_latest_model_version(name).version

    op = Operation(schema.Query)
    op.is_inference_model_ready(model_version=schema.ObjectVersionInput(name=name, version=version))
    json_data = send_graphql_request(op=op)
    result = f"/v2/models/{name}/versions/{version}/infer" if json_data["isInferenceModelReady"] else None
    return result


def set_model_version_description(name: str, version: int, description: str) -> ModelVersion:
    """
    Set model version description.

    Parameters
    ----------
    name: str
        Name of the model.
    version: int
        Version of the model.
    description: str
        Description model version.

    Returns
    -------
    ModelVersion
        Model version instance with meta information.
    """
    op = Operation(schema.Mutation)
    choice = schema.ObjectVersionInput(name=name, version=version)
    set_description = op.set_model_version_description(model_version=choice, description=description)
    set_description.name()
    set_description.version()
    set_description.description()

    model = send_graphql_request(op=op)
    return ModelVersion(model)


def set_model_version_tag(name: str, version: int, key: str, value: str) -> ModelVersion:
    """
    Set model version tag.

    Parameters
    ----------
    name: str
        Name of the model.
    version: int
        Version of the model.
    key: str
        Key tag.
    value: str
        Value tag.

    Returns
    -------
    ModelVersion
        Model version instance with meta information.
    """
    op = Operation(schema.Mutation)
    choice = schema.ObjectVersionInput(name=name, version=version)
    set_tag = op.set_model_version_tag(model_version=choice, key=key, value=value)
    set_tag.name()
    set_tag.version()
    set_tag.tags()
    model = send_graphql_request(op=op)
    return ModelVersion(model)


def delete_model_version_tag(name: str, version: int, key: str) -> ModelVersion:
    """
    Delete model version tag.

    Parameters
    ----------
    name: str
        Name of the model.
    version: int
        Version of the model.
    key: str
        Key tag.

    Returns
    -------
    ModelVersion
        Model version instance with meta information.
    """
    op = Operation(schema.Mutation)
    choice = schema.ObjectVersionInput(name=name, version=version)
    delete_tag = op.delete_model_version_tag(model_version=choice, key=key)
    delete_tag.name()
    delete_tag.version()
    delete_tag.tags()
    model = send_graphql_request(op=op)
    return ModelVersion(model)


def get_model_version_conda_env(name: str, version: int) -> dict:
    """
    Condas configuration for the model version by the model name and version.

    Parameters
    ----------
    name: str
        Name of the model.
    version: Optional[int] = None
        Version of the model. Default: None, "latest" version is used.

    Returns
    -------
    Dict
        Dict with conda configuration.
    """
    op = Operation(schema.Query)
    _model_version = schema.ObjectVersionOptionalInput(name=name, version=version)
    base_query = op.model_version_from_name_version(model_version=_model_version)
    base_query.run.get_conda_env()
    model_version = send_graphql_request(op, json_response=False)
    return model_version.model_version_from_name_version.run.get_conda_env


def get_model_version_requirements(name: str, version: int) -> list:
    """
    Requirements for the model version by the model name and version.

    Parameters
    ----------
    name: str
        Name of the model.
    version: Optional[int] = None
        Version of the model. Default: None, "latest" version is used.

    Returns
    -------
    List
        List of requirements.
    """
    op = Operation(schema.Query)
    _model_version = schema.ObjectVersionOptionalInput(name=name, version=version)
    base_query = op.model_version_from_name_version(model_version=_model_version)
    base_query.run.list_requirements()
    model_version = send_graphql_request(op, json_response=False)
    return model_version.model_version_from_name_version.run.list_requirements
