import json
from typing import Any, Dict, List
from datetime import datetime
import json
import os
from typing import Any, Dict, List
from .utils import S3_CLIENT
import re
import requests
import boto3
from typing import Dict, Any
import logging

s3 = S3_CLIENT


def version_file_path(schema_name: str) -> str:
    """Get the path to the version info file for a schema.

    Args:
        schema_name: The name of the schema.

    Returns:
        The path to the version info file for the schema.

    """
    return f"{schema_name}/{schema_name}_version_info.json"


def read_version_file(schema: str, s3=S3_CLIENT) -> Dict[str, List[Dict[str, Any]]]:
    logging.info(f"Entering read_version_file for {schema}")
    bucket: str = os.environ["RAW_BUCKET_NAME"]
    file_key: str = f"{schema}/{schema}_version_info.json"
    logging.info(
        f"Reading version info file for {schema} from S3 bucket {bucket} at {file_key}"
    )
    # Get the version info from S3
    try:
        response: Dict[str, Any] = s3.get_object(Bucket=bucket, Key=file_key)
        version_info_str: str = response["Body"].read().decode("utf-8")
        version_info: Dict[str, List[Dict[str, Any]]] = json.loads(version_info_str)
    except s3.exceptions.NoSuchKey:
        # If the file does not exist, create an empty version info structure
        version_info: Dict[str, List[Dict[str, Any]]] = {
            "tables": [{"schema_name": schema, "tables": []}]
        }

    logging.info(f"Read version info with {len(version_info['tables'])} tables")
    logging.info(f"Exiting read_version_file for {schema}")
    return version_info


def update_version_info(
    version_info: Dict,
    schema: str,
    table: str,
    file_name: str,
    file: str,
    file_size: int,
    s3_location: str,
    timestamp: str,
    fyear: str,
    upload_date: str,
) -> Dict:
    logging.info(f"Entering update_version_info for {file_name}")
    logging.debug(f"Input version_info has {len(version_info['tables'])} tables")

    # Update the version info dictionary with the file information.
    """
    Updates the version information for a file in a given schema and table.

    Args:
        - `version_info` (Dict): The current version information for the schema.
        - `schema` (str): The name of the schema.
        - `table` (str): The name of the table.
        - `file_name` (str): The name of the file.
        - `file` (str): The file itself.
        - `file_size` (int): The size of the file in bytes.
        - `timestamp` (str): The timestamp of the file.

    Returns:
        - Dict: The updated version information for the schema, with the new file version and information added.
    """
    schema_entry = get_schema_entry(version_info, schema)
    table_entry = get_table_entry(schema_entry, table)
    file_entry = update_file_entry(
        table_entry,
        file_name,
        file,
        file_size,
        s3_location,
        timestamp,
        fyear,
        upload_date,
    )  # noqa: F841, E231, E261, E501
    updated_table_entry = update_table_entry_for_the_file_with_updated_file_entry(
        table_name=table,
        file_name=file_name,
        file_entry=file_entry,
        table_entry=table_entry,
    )  # noqa: F841, E231, E261, E501
    version_info_updated = update_table_entry_of_version_info(
        version_info=version_info,
        updated_table_entry=updated_table_entry,
        table_name=table,
        schema_name=schema,
    )
    logging.debug(
        f"Updated version_info now has {len(version_info_updated['tables'])} tables"
    )
    logging.info(f"Exiting update_version_info for {file_name}")
    return version_info_updated


def initialize_version_file(file_path, s3_client):  # Add s3_client parameter here
    """This function initializes a version file. It takes a file path and an s3 client and returns nothing.

    The file path is the path to the file in the S3 bucket. The s3 client is the boto3 client that connects to S3.
    """
    version_info = {"tables": []}
    s3_client.put_object(
        Bucket=os.environ["RAW_BUCKET_NAME"],
        Key=version_file_path(file_path),
        Body=json.dumps(version_info),
    )


def update_table_entry_of_version_info(
    schema_entry: Dict, updated_table_entry: Dict, table_name: str, schema_name: str
) -> Dict:
    """Update the table entry in the version info."""
    for table in schema_entry["tables"]:
        if table["name"] == table_name:
            table.update(updated_table_entry)
            break
    else:
        schema_entry["tables"].append(updated_table_entry)

    return schema_entry


def get_schema_entry(version_info: Dict, schema: str) -> Dict:
    """
        Gets the schema entry from the version information for the given schema. If the schema does not exist in the version information, a new schema entry is created with an empty list of tables. # noqa: E501

    Args:
        - `version_info` (Dict): The current version information for the schema.
        - `schema` (str): The name of the schema.

        Returns:
        - Dict: The schema entry from the version information for the given schema. If the schema does not exist in the version information, a new schema entry is created with an empty list of tables.
    """
    schema_entry = next(
        (entry for entry in version_info["tables"] if entry["schema_name"] == schema),
        None,
    )

    # If schema_entry is None, create a new schema entry and add it to version_info
    if not schema_entry:
        schema_entry = {"schema_name": schema, "tables": []}
        version_info["tables"].append(schema_entry)

    return schema_entry


def get_table_entry(schema_entry, table_name):
    table_entry = next(
        (entry for entry in schema_entry["tables"] if entry.get("name") == table_name),
        None,
    )
    return table_entry


def get_file_entry(
    table_entry: Dict, file_name: str, file: str, file_size: int, timestamp: str
) -> Dict:
    """
    Gets the file entry from the table entry for the given file_name. If the file_name
    does not exist in the table entry, a new file entry is created with version 1 and
    the provided file information, then added to the table entry.

    Args:
        table_entry (Dict): The table entry containing the file information.
        file_name (str): The name of the file to get the entry for.
        file (str): The file itself.
        file_size (int): The size of the file in bytes.
        timestamp (str): The timestamp of the file.

    Returns:
        Dict: The file entry from the table entry for the given file_name. If the
              file_name does not exist in the table entry, a new file entry is
              created with version 1 and the provided file information, then added
              to the table entry.
    """
    file_entry = next(
        (entry for entry in table_entry["files"] if entry["file_name"] == file_name),
        None,
    )

    # If file_entry is None, create a new file entry with version 1 and add it to table_entry
    if not file_entry:
        file_entry = {
            "file_name": file_name,
            "current_version": 1,
            "versions": [
                {
                    "version": 1,
                    "timestamp": timestamp,
                    "file_size": file_size,
                    "file": file,
                },
            ],
        }
        table_entry["files"].append(file_entry)

    return file_entry


def update_file_entry(
    table_entry: Dict,
    file_name: str,
    file: str,
    file_size: int,
    s3_location: str,
    timestamp: str,
    fyear: str,
    upload_date: str,
) -> Dict:
    # Find the file_entry for the file corresponding to the given file_name.
    file_entry = next(
        (entry for entry in table_entry["files"] if entry["file_name"] == file_name),
        None,
    )

    # If file_entry is None, create a new file entry with version 1 and add it to table_entry
    if not file_entry:
        file_entry = {
            "file_name": file_name,
            "current_version": 1,
            "versions": [
                {
                    "version": 1,
                    "timestamp": timestamp,
                    "file_size": file_size,
                    "file": file,
                    "s3_location": s3_location,
                    "fyear": fyear,
                    "upload_date": upload_date,
                },
            ],
        }
        table_entry["files"].append(file_entry)
    else:
        # Check if this exact file already exists
        existing_version = next(
            (v for v in file_entry["versions"] if v["file"] == file), None
        )

        if existing_version:
            logging.info(f"File {file} already exists in {file_name}. Skipping update.")
            return file_entry

        # If the file doesn't exist, increment the current_version and add a new version entry
        file_entry["current_version"] += 1
        new_version = {
            "version": file_entry["current_version"],
            "timestamp": timestamp,
            "file_size": file_size,
            "file": file,
            "s3_location": s3_location,
            "fyear": fyear,
            "upload_date": upload_date,
        }
        file_entry["versions"].append(new_version)

    return file_entry


def update_table_entry_for_the_file_with_updated_file_entry(
    table_name, file_name, file_entry, table_entry
):
    updated_table_entry = {"table_name": table_name, "files": []}
    for fe in table_entry["files"]:
        if fe["file_name"] == file_name:
            updated_table_entry["files"].append(file_entry)
        else:
            updated_table_entry["files"].append(fe)
    return updated_table_entry


def write_version_file(schema_name: str, version_data: dict) -> None:
    """Uploads the schema version file to Amazon S3.

    Args:
        schema_name: The name of the schema.
        version_data: A dictionary of the schema version data.
    """
    try:
        bucket = os.environ["RAW_BUCKET_NAME"]
        key = f"{version_file_path(schema_name)}"
        body = json.dumps(version_data)

        logging.info(f"Uploading version file to: s3://{bucket}/{key}")
        s3.put_object(Body=body, Bucket=bucket, Key=key)
        logging.info("Successfully uploaded version file.")
    except Exception as e:
        logging.error(f"Failed to upload version file: {e}")


def update_file_info(
    table_entry: Dict,
    file_name: str,
    file: str,
    file_size: int,
    s3_location: str,
    timestamp: str,
    fyear: str,
    upload_date: str,
) -> Dict:
    """Update file information in the version tracker."""
    file_entry = check_file_name_entry(table_entry, file_name)

    if file_entry:
        if check_file_exists(file_entry, file):
            logging.info(f"File {file} already exists in {file_name}. Skipping update.")
            return table_entry
        else:
            updated_file_entry = add_file_version(
                file_entry, file, file_size, s3_location, timestamp, fyear, upload_date
            )
    else:
        updated_file_entry = create_file_name_entry(
            table_entry,
            file_name,
            file,
            file_size,
            s3_location,
            timestamp,
            fyear,
            upload_date,
        )

    return update_table_entry(table_entry, updated_file_entry)


def upload_to_s3(file_path: str, bucket_name: str, s3_key: str) -> None:
    """Uploads a file to S3."""
    s3 = boto3.client("s3")
    s3.upload_file(file_path, bucket_name, s3_key)
    logging.info(f"Uploaded: {file_path} to s3://{bucket_name}/{s3_key}")


def create_schema_entry(version_data: Dict, schema_name: str) -> Dict:
    """Create a new schema entry in the version data."""
    new_schema_entry = {"schema_name": schema_name, "tables": []}
    version_data["tables"].append(new_schema_entry)
    return new_schema_entry


def create_table_entry(schema_entry: Dict, table_name: str) -> Dict:
    """Create a new table entry in the schema entry."""
    new_table_entry = {"name": table_name, "files": []}
    schema_entry["tables"].append(new_table_entry)
    return new_table_entry


def update_version_tracker(
    schema_name: str,
    table_name: str,
    file_name: str,
    file: str,
    file_size: int,
    s3_location: str,
    timestamp: str = None,
    fyear: str = None,
    upload_date: str = None,
) -> None:
    """Main function to update the version tracker."""
    if timestamp is None:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    if fyear is None:
        fyear = f"FY{datetime.now().year}"
    if upload_date is None:
        upload_date = datetime.now().strftime("%Y-%m-%d")

    version_data = read_version_file(schema_name)
    schema_entry = get_schema_entry(version_data, schema_name)

    if not schema_entry:
        schema_entry = create_schema_entry(version_data, schema_name)

    table_entry = get_table_entry(schema_entry, table_name)

    if not table_entry:
        table_entry = create_table_entry(schema_entry, table_name)

    updated_table_entry = update_file_info(
        table_entry,
        file_name,
        file,
        file_size,
        s3_location,
        timestamp,
        fyear,
        upload_date,
    )

    updated_schema_entry = update_table_entry_of_version_info(
        schema_entry,
        updated_table_entry,
        table_name,
        schema_name,  # Added schema_name here
    )

    version_info_updated = {"tables": [updated_schema_entry]}

    write_version_file(schema_name, version_info_updated)


def check_file_name_entry(table_entry: Dict, file_name: str) -> Dict or None:
    """Check if a file_name entry exists in the table."""
    return next(
        (entry for entry in table_entry["files"] if entry["file_name"] == file_name),
        None,
    )


def check_file_exists(file_entry: Dict, file: str) -> bool:
    """Check if a specific file already exists in the versions of a file_entry."""
    return any(version["file"] == file for version in file_entry["versions"])


def create_file_name_entry(
    table_entry: Dict,
    file_name: str,
    file: str,
    file_size: int,
    s3_location: str,
    timestamp: str,
    fyear: str,
    upload_date: str,
) -> Dict:
    """Create a new file_name entry with the first version of the file."""
    new_entry = {
        "file_name": file_name,
        "current_version": 1,
        "versions": [
            {
                "version": 1,
                "timestamp": timestamp,
                "file_size": file_size,
                "file": file,
                "s3_location": s3_location,
                "fyear": fyear,
                "upload_date": upload_date,
            }
        ],
    }
    table_entry["files"].append(new_entry)
    return new_entry


def add_file_version(
    file_entry: Dict,
    file: str,
    file_size: int,
    s3_location: str,
    timestamp: str,
    fyear: str,
    upload_date: str,
) -> Dict:
    """Add a new version to an existing file_name entry."""
    file_entry["current_version"] += 1
    new_version = {
        "version": file_entry["current_version"],
        "timestamp": timestamp,
        "file_size": file_size,
        "file": file,
        "s3_location": s3_location,
        "fyear": fyear,
        "upload_date": upload_date,
    }
    file_entry["versions"].append(new_version)
    return file_entry


def update_table_entry(table_entry: Dict, file_entry: Dict) -> Dict:
    """Update the table_entry with the new or updated file_entry."""
    for i, entry in enumerate(table_entry["files"]):
        if entry["file_name"] == file_entry["file_name"]:
            table_entry["files"][i] = file_entry
            return table_entry
    table_entry["files"].append(file_entry)
    return table_entry
