"""
Unit tests for CSVLoader.
"""

import os
import tempfile
import unittest
from memory_requests.csv_loader import CSVLoader
from utils.enums import RequestType


class TestCSVLoader(unittest.TestCase):
    """Tests loading DRAM requests from CSV files."""

    def test_valid_csv_loading(self) -> None:
        loader = CSVLoader()
        
        # Create a valid temporary CSV file
        with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".csv", newline="") as temp:
            temp.write("RequestID,Operation,Address,ArrivalTime\n")
            temp.write("1,READ,0x1000,0\n")
            temp.write("2,WRITE,8192,5\n")
            temp_path = temp.name

        try:
            requests = loader.load(temp_path)
            self.assertEqual(len(requests), 2)
            
            # Request 1
            self.assertEqual(requests[0].request_id, 1)
            self.assertEqual(requests[0].operation, RequestType.READ)
            self.assertEqual(requests[0].address, 4096)  # 0x1000
            self.assertEqual(requests[0].arrival_time, 0)
            
            # Request 2
            self.assertEqual(requests[1].request_id, 2)
            self.assertEqual(requests[1].operation, RequestType.WRITE)
            self.assertEqual(requests[1].address, 8192)
            self.assertEqual(requests[1].arrival_time, 5)
        finally:
            os.remove(temp_path)

    def test_file_not_found(self) -> None:
        loader = CSVLoader()
        with self.assertRaises(FileNotFoundError):
            loader.load("non_existent_file.csv")

    def test_missing_headers(self) -> None:
        loader = CSVLoader()
        with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".csv", newline="") as temp:
            temp.write("RequestID,Address,ArrivalTime\n")  # Missing Operation
            temp.write("1,0x1000,0\n")
            temp_path = temp.name

        try:
            with self.assertRaises(ValueError) as ctx:
                loader.load(temp_path)
            self.assertIn("Missing columns", str(ctx.exception))
        finally:
            os.remove(temp_path)

    def test_invalid_operation(self) -> None:
        loader = CSVLoader()
        with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".csv", newline="") as temp:
            temp.write("RequestID,Operation,Address,ArrivalTime\n")
            temp.write("1,REFRESH,0x1000,0\n")  # Invalid operation
            temp_path = temp.name

        try:
            with self.assertRaises(ValueError) as ctx:
                loader.load(temp_path)
            self.assertIn("Invalid operation", str(ctx.exception))
        finally:
            os.remove(temp_path)


if __name__ == "__main__":
    unittest.main()
