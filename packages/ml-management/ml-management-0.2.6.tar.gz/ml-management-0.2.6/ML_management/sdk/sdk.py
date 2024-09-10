"""SDK for client library."""
import json
import locale
import posixpath
from typing import Any, Dict, List

import httpx
import pandas as pd
from jsf import JSF
from sgqlc.operation import Operation

from ML_management.mlmanagement.mlmanagement import get_server_url
from ML_management.mlmanagement.session import AuthSession
from ML_management.mlmanagement.variables import _get_s3_gateway_url
from ML_management.mlmanagement.visibility_options import VisibilityOptions


def _to_datetime(df: pd.DataFrame, column_names: List[str]) -> pd.DataFrame:
    """
    Convert df's columns to datetime.

    Parameters
    ----------
    df: pd.DataFrame
        pd.DataFrame in which the columns will be converted.
    column_names: List[str]
        Column names to be converted.

    Returns
    -------
    pd.DataFrame
        Pandas dataframe with converted columns.
    """
    for column_name in column_names:
        df[column_name] = pd.to_datetime(df[column_name], unit="s")

    return df


def send_graphql_request(op: Operation, json_response: bool = True) -> Any:
    """Send request to server and process the response."""
    json_data = AuthSession().sgqlc_request(op)

    if "data" not in json_data or json_data["data"] is None:
        server_url = get_server_url()
        try:
            if locale.getdefaultlocale()[0][:2] == "ru":
                url_base = posixpath.join(server_url, "locales/ru/ru.json")
            else:
                url_base = posixpath.join(server_url, "locales/en/en.json")
        except Exception:
            # if there is no locale file use english by default.
            url_base = posixpath.join(server_url, "locales/en/en.json")
        translation = httpx.get(url_base).json()

        error_message = json_data["errors"][0]["message"]

        try:
            message_type, message_value = error_message.split(".")
        except Exception:
            raise Exception(error_message) from None

        if message_type not in translation:
            raise Exception(message_type)

        formatted_translated_message = translation[message_type][message_value]
        if (
            ("extensions" in json_data["errors"][0])
            and ("params" in json_data["errors"][0]["extensions"])
            and (json_data["errors"][0]["extensions"]["params"] is not None)
        ):
            raise Exception(
                formatted_translated_message.format().format(**json_data["errors"][0]["extensions"]["params"])
            )
        raise Exception(formatted_translated_message)

    if json_response:
        return json_data["data"]
    else:
        return op + json_data


def update_bucket_visibility(bucket_name: str, new_visibility: VisibilityOptions) -> None:
    with AuthSession().post(
        posixpath.join(_get_s3_gateway_url(), "update-bucket-auth", bucket_name),
        json={"visibility": new_visibility.value},
    ) as response:
        response.raise_for_status()
        print("Visibility successfully updated")


def _generate_fake_schema(json_schema: dict) -> dict:
    if "required" not in json_schema.keys():
        return {}

    required_properties = {key: json_schema["properties"][key] for key in json_schema["required"]}
    json_schema["properties"] = required_properties

    faker = JSF(json_schema)
    fake_json = faker.generate()
    return fake_json


def _print_params_by_schema(json_schema: Dict, schema_type: str) -> None:
    """Print entity JSON Schema and example with required params."""
    properties_and_required_dict = {key: json_schema[key] for key in ("properties", "required") if key in json_schema}

    json_formatted_str = json.dumps(properties_and_required_dict, indent=2)

    print(f"{schema_type} json-schema:")

    print(json_formatted_str)

    print(f"{schema_type} parameters example:")

    fake_json = _generate_fake_schema(json_schema)

    print(fake_json)
