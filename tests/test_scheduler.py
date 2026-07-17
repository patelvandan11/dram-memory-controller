# test_scheduler.py
import unittest

from controller.scheduler import FCFSScheduler
from memory_requests.memory_request import MemoryRequest
from utils.enums import RequestType


class TestFCFSScheduler(unittest.TestCase):
    """Unit tests for the FCFS scheduler."""

    def setUp(self) -> None:
        self.scheduler = FCFSScheduler()

    def create_request(self, request_id: int) -> MemoryRequest:
        return MemoryRequest(
            request_id=request_id,
            address=0x1000 + request_id,
            row=request_id,
            column=0,
            bank=0,
            operation=RequestType.READ,
            arrival_time=request_id,
        )

    def test_add_request(self) -> None:
        request = self.create_request(1)

        self.scheduler.add_request(request)

        self.assertEqual(self.scheduler.queue_length(), 1)

    def test_remove_request(self) -> None:
        request = self.create_request(1)

        self.scheduler.add_request(request)

        removed = self.scheduler.get_next_request()
        self.assertEqual(removed.request_id, 1)

    def test_fcfs_order(self) -> None:
        for i in range(5):
            self.scheduler.add_request(self.create_request(i))

        for i in range(5):
            request = self.scheduler.get_next_request()
            self.assertEqual(request.request_id, i)

    def test_peek(self) -> None:
        request = self.create_request(5)

        self.scheduler.add_request(request)

        self.assertEqual(
            self.scheduler.peek_next_request().request_id,
            5,
        )

        self.assertEqual(self.scheduler.queue_length(), 1)

    def test_empty_queue(self) -> None:
        self.assertIsNone(self.scheduler.get_next_request())
        self.scheduler.peek_request()
        self.assertEqual(self.scheduler.queue_length(), 0)


if __name__ == "__main__":
    unittest.main()