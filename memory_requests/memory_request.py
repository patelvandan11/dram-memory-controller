"""
Memory request representation for the DRAM Memory Controller Simulator.
"""

from dataclasses import dataclass
from typing import Optional

from utils.enums import RequestStatus, RequestType


@dataclass
class MemoryRequest:
    """
    Represents a single CPU memory request.

    Attributes:
        request_id: Unique request identifier.
        address: Physical memory address.
        row: Target DRAM row.
        column: Target DRAM column.
        bank: Target DRAM bank.
        operation: Memory operation (READ or WRITE).
        arrival_time: Cycle when the request entered the controller.
        start_time: Cycle when servicing began.
        finish_time: Cycle when servicing completed.
        latency: Total request latency.
        status: Current request state.
    """

    request_id: int
    address: int

    row: int
    column: int
    bank: int

    operation: RequestType

    arrival_time: int

    start_time: Optional[int] = None
    finish_time: Optional[int] = None
    latency: Optional[int] = None

    status: RequestStatus = RequestStatus.WAITING

    def __post_init__(self) -> None:
        """
        Validate request fields after initialization.
        """

        if self.request_id < 0:
            raise ValueError("Request ID must be non-negative.")

        if self.address < 0:
            raise ValueError("Address must be non-negative.")

        if self.row < 0:
            raise ValueError("Row must be non-negative.")

        if self.column < 0:
            raise ValueError("Column must be non-negative.")

        if self.bank < 0:
            raise ValueError("Bank must be non-negative.")

        if self.arrival_time < 0:
            raise ValueError("Arrival time must be non-negative.")

        if not isinstance(self.operation, RequestType):
            raise TypeError("Operation must be a RequestType.")

        if not isinstance(self.status, RequestStatus):
            raise TypeError("Status must be a RequestStatus.")

    def __str__(self) -> str:
        """
        Return a readable string representation of the request.
        """

        return (
            f"MemoryRequest("
            f"id={self.request_id}, "
            f"op={self.operation.name}, "
            f"addr=0x{self.address:X}, "
            f"bank={self.bank}, "
            f"row={self.row}, "
            f"col={self.column}, "
            f"status={self.status.name}, "
            f"arrival={self.arrival_time}, "
            f"start={self.start_time}, "
            f"finish={self.finish_time}, "
            f"latency={self.latency})"
        )