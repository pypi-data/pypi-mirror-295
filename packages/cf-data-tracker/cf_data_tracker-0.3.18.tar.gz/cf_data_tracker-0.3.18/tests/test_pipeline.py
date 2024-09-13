import os
from datetime import datetime, timedelta
import random
from dotenv import load_dotenv
from cf_data_tracker.raw_tracker import update_version_tracker, upload_to_s3

# Load environment variables
load_dotenv()

# Mock schema and table
SCHEMA_NAME = "pharmacy_data"
TABLE_NAME = "prescriptions"

# S3 bucket
S3_BUCKET = os.getenv("AWS_DEST_BUCKET_RAW")

def generate_mock_file(year, month):
    """Generate a mock file name and content."""
    file_name = f"prescriptions_{year}_{month:02d}.csv"
    content = f"Mock prescription data for {year}-{month:02d}"
    return file_name, content

def mock_upload_and_track(year, month):
    """Simulate file upload and version tracking."""
    file_name, content = generate_mock_file(year, month)
    
    # Simulate file upload
    s3_key = f"{SCHEMA_NAME}/{TABLE_NAME}/{file_name}"
    file_size = len(content)
    s3_location = f"s3://{S3_BUCKET}/{s3_key}"
    
    # In a real scenario, you would upload the file here
    # For this mock, we'll just print the upload info
    print(f"Uploading {file_name} to {s3_location}")
    # upload_to_s3(file_path, S3_BUCKET, s3_key)  # Uncomment this in a real scenario
    
    # Update version tracker
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    fyear = f"FY{year}" if month > 6 else f"FY{year-1}"
    upload_date = datetime.now().strftime("%Y-%m-%d")
    
    update_version_tracker(
        schema_name=SCHEMA_NAME,
        table_name=TABLE_NAME,
        file_name=file_name,
        file=file_name,
        file_size=file_size,
        s3_location=s3_location,
        timestamp=timestamp,
        fyear=fyear,
        upload_date=upload_date
    )
    
    print(f"Updated version tracker for {file_name}")

def run_mock_pipeline():
    """Run the mock pipeline for the last 12 months."""
    current_date = datetime.now()
    for i in range(12):
        date = current_date - timedelta(days=30*i)
        year = date.year
        month = date.month
        mock_upload_and_track(year, month)

if __name__ == "__main__":
    run_mock_pipeline()