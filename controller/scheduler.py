from abc import ABC, abstractmethod
from collections import deque
from typing import Optional

from memory_requests.memory_request import MemoryRequest


# ------------------------------------------------------
# Base Scheduler
# ------------------------------------------------------

class BaseScheduler(ABC):

    @abstractmethod
    def add_request(self, request: MemoryRequest):
        pass

    @abstractmethod
    def get_next_request(self):
        pass

    @abstractmethod
    def queue_length(self):
        pass


# ------------------------------------------------------
# FCFS Scheduler
# ------------------------------------------------------

class FCFSScheduler(BaseScheduler):

    def __init__(self):
        self.queue = deque()

    def add_request(self, request):
        self.queue.append(request)

    def get_next_request(self):
        if not self.queue:
            return None
        return self.queue.popleft()

    # Backward compatibility
    def remove_request(self):
        return self.get_next_request()

    def peek_request(self):
        if not self.queue:
            return None
        return self.queue[0]

    def peek_next_request(self):
        return self.peek_request()

    def queue_length(self):
        return len(self.queue)


# ------------------------------------------------------
# FR-FCFS Scheduler
# ------------------------------------------------------

class FRFCFSScheduler(BaseScheduler):

    def __init__(self):
        self.queue = []

    def add_request(self, request):
        self.queue.append(request)

    def queue_length(self):
        return len(self.queue)

    def peek_request(self):
        if not self.queue:
            return None
        return self.queue[0]

    def peek_next_request(self):
        return self.peek_request()

    def remove_request(self, open_row: Optional[int] = None):
        return self.get_next_request(open_row)

    def get_next_request(self, open_row = None):

        if not self.queue:
            return None

        # Step 1: Prioritize row buffer hits
        if open_row is not None:
            if isinstance(open_row, dict):
                row_hits = [
                    req
                    for req in self.queue
                    if open_row.get(req.bank) is not None and req.row == open_row.get(req.bank)
                ]
            else:
                row_hits = [
                    req
                    for req in self.queue
                    if req.row == open_row
                ]

            if row_hits:
                oldest = min(
                    row_hits,
                    key=lambda r: r.arrival_time
                )

                self.queue.remove(oldest)
                return oldest

        # Step 2: FCFS (oldest request)
        oldest = min(
            self.queue,
            key=lambda r: r.arrival_time
        )

        self.queue.remove(oldest)
        return oldest