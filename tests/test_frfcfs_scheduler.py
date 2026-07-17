# test_frfcfs_scheduler.py\
    
import unittest

from controller.scheduler import FRFCFSScheduler
from memory_requests.memory_request import MemoryRequest
from utils.enums import RequestType


class TestFRFCFS(unittest.TestCase):

    def create(self, idx, row, arrival):

        return MemoryRequest(
            request_id=idx,
            operation=RequestType.READ,
            address=0,
            bank=0,
            row=row,
            column=0,
            arrival_time=arrival,
        )

    def test_row_hit_priority(self):

        scheduler = FRFCFSScheduler()

        scheduler.add_request(self.create(1, 5, 0))
        scheduler.add_request(self.create(2, 8, 1))
        scheduler.add_request(self.create(3, 5, 2))

        request = scheduler.get_next_request(
            open_row=5
        )

        self.assertEqual(
            request.request_id,
            1
        )

        request = scheduler.get_next_request(
            open_row=5
        )

        self.assertEqual(
            request.request_id,
            3
        )

    def test_fcfs_when_no_hit(self):

        scheduler = FRFCFSScheduler()

        scheduler.add_request(self.create(1, 4, 2))
        scheduler.add_request(self.create(2, 8, 0))

        request = scheduler.get_next_request(
            open_row=10
        )

        self.assertEqual(
            request.request_id,
            2
        )


if __name__ == "__main__":
    unittest.main()