import unittest
from unittest import mock
from datetime import datetime
from cf_data_tracker.raw_tracker import (
    check_file_name_entry,
    check_file_exists,
    create_file_name_entry,
    add_file_version,
    update_table_entry,
    update_file_info,
    update_version_tracker,
)

class TestRawTracker(unittest.TestCase):

    def setUp(self):
        # Sample data for testing
        self.sample_table_entry = {
            "files": [
                {
                    "file_name": "HES_APC_2022",
                    "current_version": 1,
                    "versions": [
                        {
                            "version": 1,
                            "timestamp": "2023-01-01",
                            "file_size": 1000,
                            "file": "HES_APC_202201.zip",
                            "s3_location": "s3://bucket/HES_APC_202201.zip",
                            "fyear": "FY2022",
                            "upload_date": "2023-01-01",
                        }
                    ]
                }
            ]
        }

    def test_check_file_name_entry(self):
        result = check_file_name_entry(self.sample_table_entry, "HES_APC_2022")
        self.assertIsNotNone(result)
        self.assertEqual(result["file_name"], "HES_APC_2022")

        result = check_file_name_entry(self.sample_table_entry, "NonExistent")
        self.assertIsNone(result)

    def test_check_file_exists(self):
        file_entry = self.sample_table_entry["files"][0]
        self.assertTrue(check_file_exists(file_entry, "HES_APC_202201.zip"))
        self.assertFalse(check_file_exists(file_entry, "NonExistent.zip"))

    def test_create_file_name_entry(self):
        new_entry = create_file_name_entry(
            self.sample_table_entry,
            "HES_APC_2023",
            "HES_APC_202301.zip",
            2000,
            "s3://bucket/HES_APC_202301.zip",
            "2023-02-01",
            "FY2023",
            "2023-02-01"
        )
        self.assertEqual(new_entry["file_name"], "HES_APC_2023")
        self.assertEqual(new_entry["current_version"], 1)
        self.assertEqual(len(new_entry["versions"]), 1)

    def test_add_file_version(self):
        file_entry = self.sample_table_entry["files"][0]
        updated_entry = add_file_version(
            file_entry,
            "HES_APC_202202.zip",
            2000,
            "s3://bucket/HES_APC_202202.zip",
            "2023-02-01",
            "FY2022",
            "2023-02-01"
        )
        self.assertEqual(updated_entry["current_version"], 2)
        self.assertEqual(len(updated_entry["versions"]), 2)

    def test_update_table_entry(self):
        new_file_entry = {
            "file_name": "HES_APC_2023",
            "current_version": 1,
            "versions": [
                {
                    "version": 1,
                    "timestamp": "2023-02-01",
                    "file_size": 2000,
                    "file": "HES_APC_202301.zip",
                    "s3_location": "s3://bucket/HES_APC_202301.zip",
                    "fyear": "FY2023",
                    "upload_date": "2023-02-01",
                }
            ]
        }
        updated_table = update_table_entry(self.sample_table_entry, new_file_entry)
        self.assertEqual(len(updated_table["files"]), 2)

    def test_update_file_info(self):
        updated_table = update_file_info(
            self.sample_table_entry,
            "HES_APC_2022",
            "HES_APC_202202.zip",
            2000,
            "s3://bucket/HES_APC_202202.zip",
            "2023-02-01",
            "FY2022",
            "2023-02-01"
        )
        self.assertEqual(updated_table["files"][0]["current_version"], 2)
        self.assertEqual(len(updated_table["files"][0]["versions"]), 2)

    @unittest.mock.patch('cf_data_tracker.raw_tracker.read_version_file')
    @unittest.mock.patch('cf_data_tracker.raw_tracker.write_version_file')
    def test_update_version_tracker(self, mock_write, mock_read):
        mock_read.return_value = {
            "tables": [{
                "schema_name": "test",
                "tables": [{
                    "name": "APC",
                    "files": self.sample_table_entry["files"]
                }]
            }]
        }
        
        update_version_tracker(
            "test",
            "APC",
            "HES_APC_2022",
            "HES_APC_202202.zip",
            2000,
            "s3://bucket/HES_APC_202202.zip"
        )

        mock_write.assert_called_once()
        written_data = mock_write.call_args[0][1]
        self.assertEqual(written_data["tables"][0]["tables"][0]["files"][0]["current_version"], 2)

if __name__ == '__main__':
    unittest.main()