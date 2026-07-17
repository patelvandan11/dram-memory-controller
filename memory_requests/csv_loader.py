"""
CSV request loader.

Reads request traces and converts them into MemoryRequest objects.
"""

from __future__ import annotations

import csv
from pathlib import Path

from config.config import CONFIG
from memory_requests.memory_request import MemoryRequest
from utils.enums import RequestType


REQUIRED_COLUMNS = (
    "RequestID",
    "Operation",
    "Address",
    "ArrivalTime",
)


class CSVLoader:
    """
    Loads memory requests from CSV.
    """

    def __init__(self, config=CONFIG):
        self.config = config

    def load(self, filename: str) -> list[MemoryRequest]:

        path = Path(filename)

        if not path.exists():
            raise FileNotFoundError(
                f"CSV file not found: {filename}"
            )

        requests: list[MemoryRequest] = []

        with path.open(
            newline="",
            encoding="utf-8"
        ) as csvfile:

            reader = csv.DictReader(csvfile)

            self._validate_header(reader.fieldnames)

            for line_number, row in enumerate(
                reader,
                start=2
            ):

                try:

                    request = self._parse_row(row)

                    requests.append(request)

                except Exception as exc:

                    raise ValueError(
                        f"Line {line_number}: {exc}"
                    ) from exc

        return requests

    def _validate_header(self, headers):

        if headers is None:
            raise ValueError("CSV file is empty.")

        missing = [
            col
            for col in REQUIRED_COLUMNS
            if col not in headers
        ]

        if missing:
            raise ValueError(
                f"Missing columns: {missing}"
            )

    def _parse_row(self, row):

        request_id = int(row["RequestID"])

        operation = row["Operation"].strip().upper()

        if operation == "READ":
            op = RequestType.READ

        elif operation == "WRITE":
            op = RequestType.WRITE

        else:
            raise ValueError(
                f"Invalid operation '{operation}'"
            )

        address = self._parse_address(
            row["Address"]
        )

        arrival = int(
            row["ArrivalTime"]
        )

        bank, row_id, column = self._map_address(
            address
        )

        return MemoryRequest(
            request_id=request_id,
            address=address,
            bank=bank,
            row=row_id,
            column=column,
            operation=op,
            arrival_time=arrival,
        )

    @staticmethod
    def _parse_address(value: str) -> int:

        value = value.strip()

        if value.lower().startswith("0x"):
            return int(value, 16)

        return int(value)

    def _map_address(self, address: int):

        column = (
            address %
            self.config.COLUMN_SIZE
        )

        row = (
            address //
            self.config.COLUMN_SIZE
        ) % self.config.ROW_SIZE

        bank = (
            address //
            (
                self.config.COLUMN_SIZE *
                self.config.ROW_SIZE
            )
        ) % self.config.NUM_BANKS

        return bank, row, column