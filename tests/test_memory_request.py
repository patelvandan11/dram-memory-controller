import unittest

from memory_requests.memory_request import MemoryRequest
from utils.enums import RequestStatus, RequestType


class TestMemoryRequest(unittest.TestCase):
    """Unit tests for the MemoryRequest class."""

    def test_valid_request(self) -> None:
        """Verify a valid request is created correctly."""

        request = MemoryRequest(
            request_id=1,
            address=0x1000,
            row=20,
            column=8,
            bank=1,
            operation=RequestType.READ,
            arrival_time=5,
        )

        self.assertEqual(request.request_id, 1)
        self.assertEqual(request.status, RequestStatus.WAITING)
        self.assertEqual(request.operation, RequestType.READ)

    def test_negative_address(self) -> None:
        """Negative addresses should raise ValueError."""

        with self.assertRaises(ValueError):
            MemoryRequest(
                request_id=1,
                address=-1,
                row=0,
                column=0,
                bank=0,
                operation=RequestType.READ,
                arrival_time=0,
            )

    def test_negative_request_id(self) -> None:
        """Negative request IDs should raise ValueError."""

        with self.assertRaises(ValueError):
            MemoryRequest(
                request_id=-5,
                address=100,
                row=0,
                column=0,
                bank=0,
                operation=RequestType.WRITE,
                arrival_time=0,
            )

    def test_string_representation(self) -> None:
        """The string representation should include key fields."""

        request = MemoryRequest(
            request_id=3,
            address=0x200,
            row=4,
            column=2,
            bank=0,
            operation=RequestType.WRITE,
            arrival_time=10,
        )

        output = str(request)

        self.assertIn("WRITE", output)
        self.assertIn("id=3", output)
        self.assertIn("status=WAITING", output)


if __name__ == "__main__":
    unittest.main()