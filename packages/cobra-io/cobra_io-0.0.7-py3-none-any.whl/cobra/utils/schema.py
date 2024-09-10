import json
from pathlib import Path
from typing import Dict, Tuple

from jsonschema.protocols import Validator
import jsonschema.validators
import referencing
import referencing.exceptions

from cobra.utils.caches import SCHEMA_CACHE
from cobra.utils.configurations import COBRA_VERSION
from cobra.utils.requests import session
from cobra.utils.urls import SCHEMA_URL


def retrieve_schema_uri(schema_uri: str) -> referencing.Resource:
    """Retrieve a schema from a URI; cached via session."""
    response = session.get(schema_uri)
    if response.status_code != 200:
        raise referencing.exceptions.NoSuchResource(schema_uri)
    return referencing.Resource.from_contents(response.json())


"""
Registry for all referenced schemas using global session to manage caching and retries.
"""


SCHEMA_REGISTRY = referencing.Registry(retrieve=retrieve_schema_uri)


def get_schema(schema: str, version: str = COBRA_VERSION, force_download: bool = False) -> Path:
    """
    Download a schema from the CoBRA API

    :param schema: The schema to download.
    :param version: The version of CoBRA to download from.
    :param force_download: Whether to force a download even if the schema is already cached.
    :return: The path to the downloaded schema.
    """
    if version != COBRA_VERSION:
        raise NotImplementedError
    schema_file = SCHEMA_CACHE.joinpath(f"{schema}.json")
    if not force_download and schema_file.exists():
        return schema_file
    r = session.get(SCHEMA_URL + f"{schema}.json")
    if r.status_code != 200:
        raise ValueError(f"Could not get schema {schema} from CoBRA (error {r.status_code}).")
    schema_file.write_text(r.text)
    return schema_file


def get_schema_validator(schema: str, version: str = COBRA_VERSION,
                         force_download: bool = False) -> Tuple[Dict, Validator]:
    """Return a loaded schema and a validator for it. Retrieval is done via get_schema."""
    schema_file = get_schema(schema, version, force_download)
    with open(schema_file) as f:
        main_schema = json.load(f)

    # Allow also tuple as json array
    new_type_checker = jsonschema.Draft202012Validator.TYPE_CHECKER.redefine(
        "array", lambda _, instance:
        jsonschema.Draft202012Validator.TYPE_CHECKER.is_type(instance, "array") or isinstance(instance, tuple))
    validator_with_tuple = jsonschema.validators.extend(jsonschema.Draft202012Validator, type_checker=new_type_checker)
    validator = validator_with_tuple(main_schema, registry=SCHEMA_REGISTRY)

    return main_schema, validator
