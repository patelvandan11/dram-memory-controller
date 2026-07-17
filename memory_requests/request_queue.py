"""
Request Queue Module

Stores memory requests before they are scheduled by the
memory controller.
"""

from collections import deque
from typing import Optional

from memory_requests.memory_request import MemoryRequest


class RequestQueue:
    """
    FIFO queue for memory requests.
    """

    def __init__(self, max_size: int = 64):
        """
        Initialize the request queue.

        Args:
            max_size: Maximum number of requests allowed.
        """
        self._queue = deque()
        self.max_size = max_size

    def enqueue(self, request: MemoryRequest) -> None:
        """
        Add a request to the queue.

        Raises:
            OverflowError: If the queue is full.
            TypeError: If the object is not a MemoryRequest.
        """

        if not isinstance(request, MemoryRequest):
            raise TypeError(
                "Only MemoryRequest objects can be added."
            )

        if self.is_full():
            raise OverflowError(
                "Request queue is full."
            )

        self._queue.append(request)

    def dequeue(self) -> MemoryRequest:
        """
        Remove and return the oldest request.

        Raises:
            IndexError: If the queue is empty.
        """

        if self.is_empty():
            raise IndexError(
                "Request queue is empty."
            )

        return self._queue.popleft()

    def peek(self) -> Optional[MemoryRequest]:
        """
        Return the next request without removing it.
        """

        if self.is_empty():
            return None

        return self._queue[0]

    def is_empty(self) -> bool:
        """
        Returns True if the queue is empty.
        """
        return len(self._queue) == 0

    def is_full(self) -> bool:
        """
        Returns True if the queue is full.
        """
        return len(self._queue) >= self.max_size

    def size(self) -> int:
        """
        Current number of requests.
        """
        return len(self._queue)

    def clear(self) -> None:
        """
        Remove all requests.
        """
        self._queue.clear()

    def get_all(self) -> list[MemoryRequest]:
        """
        Return all queued requests.
        """

        return list(self._queue)

    def __len__(self):
        return len(self._queue)

    def __iter__(self):
        return iter(self._queue)

    def __repr__(self):

        return (
            f"RequestQueue("
            f"size={self.size()}, "
            f"max_size={self.max_size})"
        )