import json
import os
from typing import Dict, List, Any
from datetime import datetime
import pandas as pd
from .utils import S3_CLIENT

def read_clean_version_tracker(clean_bucket: str, tracker_path: str) -> Dict:
    """Read the clean version tracker from S3."""
    try:
        response = S3_CLIENT.get_object(Bucket=clean_bucket, Key=tracker_path)
        clean_tracker = json.loads(response['Body'].read().decode('utf-8'))
        return clean_tracker
    except S3_CLIENT.exceptions.NoSuchKey:
        return {"schema_name": tracker_path.split('/')[0], "tables": {}}

def write_clean_version_tracker(clean_bucket: str, tracker_path: str, clean_tracker: Dict) -> None:
    """Write the clean version tracker to S3."""
    S3_CLIENT.put_object(
        Bucket=clean_bucket,
        Key=tracker_path,
        Body=json.dumps(clean_tracker, indent=2)
    )

def get_version_info(versions: List[Dict[str, Any]], version: int) -> Dict[str, Any]:
    """Get the version info for a specific version."""
    return next((v for v in versions if v["version"] == version), None)

def delete_outdated_parquets(clean_bucket: str, schema: str, table_name: str, file_name: str) -> None:
    """Delete outdated parquet files from S3."""
    prefix = f"{schema}/{table_name}/{file_name.replace('.zip', '')}"
    objects_to_delete = []
    
    paginator = S3_CLIENT.get_paginator('list_objects_v2')
    pages = paginator.paginate(Bucket=clean_bucket, Prefix=prefix)
    
    for page in pages:
        if 'Contents' in page:
            for obj in page['Contents']:
                objects_to_delete.append({'Key': obj['Key']})
    
    if objects_to_delete:
        S3_CLIENT.delete_objects(
            Bucket=clean_bucket,
            Delete={'Objects': objects_to_delete}
        )

def update_and_write_clean_version_info(
    schema: str,
    clean_bucket: str,
    clean_version: Dict,
    file: Dict,
    table_name: str,
    latest_version_info: Dict,
    new_parquet_files: List[str]
) -> Dict:
    """Update and write the clean version info."""
    if table_name not in clean_version["tables"]:
        clean_version["tables"][table_name] = {}
    
    file_name = file["file_name"]
    current_version = file["current_version"]
    
    clean_version["tables"][table_name][file_name] = {
        "file_info": {
            "version": current_version,
            "timestamp": datetime.now().isoformat(),
            "file_size": latest_version_info["file_size"],
            "s3_location": latest_version_info["s3_location"],
            "fyear": latest_version_info.get("fyear"),
            "upload_date": latest_version_info.get("upload_date")
        },
        "clean_files": new_parquet_files
    }
    
    write_clean_version_tracker(clean_bucket, f"{schema}/{schema}_clean_version_info.json", clean_version)
    return clean_version

def get_clean_file_info(clean_tracker: Dict, table_name: str, file_name: str) -> Dict:
    """Get clean file info from the clean tracker."""
    return clean_tracker.get("tables", {}).get(table_name, {}).get(file_name, {}).get("file_info", {})

def get_clean_files(clean_tracker: Dict, table_name: str, file_name: str) -> List[str]:
    """Get clean files from the clean tracker."""
    return clean_tracker.get("tables", {}).get(table_name, {}).get(file_name, {}).get("clean_files", [])

# New functions

def save_to_parquet(df: pd.DataFrame, path: str) -> None:
    """Save a DataFrame to a parquet file."""
    df.to_parquet(path, engine='pyarrow')

def upload_to_s3(file_name: str, bucket: str, object_name: str) -> None:
    """Upload a file to S3."""
    try:
        S3_CLIENT.upload_file(file_name, bucket, object_name)
    except Exception as e:
        print(f"Error uploading {file_name} to S3: {e}")

def process_and_upload_data(
    df: pd.DataFrame,
    clean_bucket: str,
    schema: str,
    table_name: str,
    file_name: str,
    group_by_column: str = None
) -> List[str]:
    """Process and upload data to S3 in parquet format."""
    uploaded_files = []

    if group_by_column:
        grouped = df.groupby(group_by_column)
        for name, group in grouped:
            parquet_file_name = f"{name}.parquet"
            local_path = os.path.join("/tmp", parquet_file_name)
            s3_object_name = f"{schema}/{table_name}/{parquet_file_name}"
            
            save_to_parquet(group, local_path)
            upload_to_s3(local_path, clean_bucket, s3_object_name)
            uploaded_files.append(s3_object_name)
            os.remove(local_path)  # remove the local file
    else:
        parquet_file_name = f"{file_name}.parquet"
        local_path = os.path.join("/tmp", parquet_file_name)
        s3_object_name = f"{schema}/{table_name}/{parquet_file_name}"
        
        save_to_parquet(df, local_path)
        upload_to_s3(local_path, clean_bucket, s3_object_name)
        uploaded_files.append(s3_object_name)
        os.remove(local_path)  # remove the local file

    return uploaded_files