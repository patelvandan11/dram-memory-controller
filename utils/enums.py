"""
Common enumerations used throughout the simulator.
"""

from enum import Enum


class RequestType(Enum):
    """Represents the type of memory request."""

    READ = "READ"
    WRITE = "WRITE"


class RequestStatus(Enum):
    """Represents the lifecycle of a memory request."""

    WAITING = "WAITING"
    SCHEDULED = "SCHEDULED"
    COMPLETED = "COMPLETED"