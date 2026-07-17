import unittest

from memory_requests.request_queue import RequestQueue
from memory_requests.memory_request import MemoryRequest
from utils.enums import RequestType


class TestRequestQueue(unittest.TestCase):

    def setUp(self):

        self.queue = RequestQueue(max_size=2)

        self.req1 = MemoryRequest(
            request_id=1,
            operation=RequestType.READ,
            address=0,
            bank=0,
            row=0,
            column=0,
            arrival_time=0,
        )

        self.req2 = MemoryRequest(
            request_id=2,
            operation=RequestType.WRITE,
            address=64,
            bank=0,
            row=0,
            column=64,
            arrival_time=1,
        )

    def test_enqueue(self):

        self.queue.enqueue(self.req1)

        self.assertEqual(
            self.queue.size(),
            1
        )

    def test_dequeue(self):

        self.queue.enqueue(self.req1)

        request = self.queue.dequeue()

        self.assertEqual(
            request.request_id,
            1
        )

    def test_peek(self):

        self.queue.enqueue(self.req1)

        self.assertEqual(
            self.queue.peek().request_id,
            1
        )

        self.assertEqual(
            self.queue.size(),
            1
        )

    def test_is_empty(self):

        self.assertTrue(
            self.queue.is_empty()
        )

    def test_queue_full(self):

        self.queue.enqueue(self.req1)
        self.queue.enqueue(self.req2)

        with self.assertRaises(OverflowError):
            self.queue.enqueue(self.req1)

    def test_dequeue_empty(self):

        with self.assertRaises(IndexError):
            self.queue.dequeue()


if __name__ == "__main__":
    unittest.main()