"""
Memory Controller Module
========================

Handles memory request scheduling, bank management, and timing constraint enforcement.
"""

from typing import Optional, Dict
from config.config import CONFIG
from controller.scheduler import BaseScheduler, FRFCFSScheduler
from memory_requests.memory_request import MemoryRequest
from utils.enums import RequestStatus, RequestType
from timing.timing_checker import TimingChecker
from simulation_stats.metrics import Metrics
from simulation.dram_bank import DRAMBank


class MemoryController:
    """
    Simulates a DRAM memory controller.
    
    Coordinates between the scheduler, the timing checker, and individual banks.
    Processes requests cycle-by-cycle.
    """

    def __init__(self, scheduler: BaseScheduler, metrics: Metrics):
        """
        Initialize the memory controller.

        Args:
            scheduler: The scheduling policy to use.
            metrics: The metrics object to log events.
        """
        self.scheduler: BaseScheduler = scheduler
        self.metrics: Metrics = metrics
        self.timing_checker: TimingChecker = TimingChecker()

        # Initialize all DRAM banks
        self.banks: Dict[int, DRAMBank] = {
            i: DRAMBank(i) for i in range(CONFIG.NUM_BANKS)
        }

        # Request currently being serviced
        self.current_request: Optional[MemoryRequest] = None

        # Cycle at which the active command finishes servicing
        self.completion_cycle: Optional[int] = None

        # Track what stage of command sequence we are in for logging/debugging
        self.current_stage: Optional[str] = None

    def add_request(self, request: MemoryRequest) -> None:
        """
        Add a request to the controller.

        Args:
            request: The memory request to add.
        """
        request.status = RequestStatus.WAITING
        self.scheduler.add_request(request)
        self.metrics.record_request(request.operation == RequestType.READ)

    def step(self, current_cycle: int) -> None:
        """
        Advance the memory controller state by one clock cycle.

        Args:
            current_cycle: The current simulation cycle.
        """
        # 1. Handle completion of in-progress READ/WRITE command
        if self.current_request is not None and self.completion_cycle is not None:
            if current_cycle >= self.completion_cycle:
                req = self.current_request
                req.finish_time = current_cycle
                req.latency = req.finish_time - req.arrival_time
                req.status = RequestStatus.COMPLETED

                # Record completion in metrics
                self.metrics.record_completion(req.latency)
                self.metrics.record_bank_access(req.bank)

                # Reset state
                self.current_request = None
                self.completion_cycle = None
                self.current_stage = None

        # 2. If no request is being processed, fetch next request from scheduler
        if self.current_request is None:
            if isinstance(self.scheduler, FRFCFSScheduler):
                open_rows = {
                    bank_id: bank.open_row for bank_id, bank in self.banks.items()
                }
                self.current_request = self.scheduler.get_next_request(open_row=open_rows)
            else:
                self.current_request = self.scheduler.get_next_request()

            if self.current_request is not None:
                self.current_request.status = RequestStatus.SCHEDULED
                self.current_request.start_time = current_cycle
                self.current_stage = "START"

        # 3. Process the current request by issuing the appropriate DRAM commands
        if self.current_request is not None and self.completion_cycle is None:
            req = self.current_request
            bank = self.banks[req.bank]

            if bank.open_row is not None and bank.open_row != req.row:
                # Row Buffer Conflict: must precharge the bank first
                if self.timing_checker.can_precharge(req.bank, current_cycle):
                    self.timing_checker.precharge(req.bank, current_cycle)
                    bank.precharge()
                    self.current_stage = "PRECHARGING"
            elif bank.open_row is None:
                # Bank is closed: must activate the target row
                if self.timing_checker.can_activate(req.bank, current_cycle):
                    self.timing_checker.activate(req.bank, current_cycle)
                    bank.activate(req.row)
                    self.current_stage = "ACTIVATING"
            else:
                # Row Buffer Hit: issue the READ or WRITE command
                if req.operation == RequestType.READ:
                    if self.timing_checker.can_read(req.bank, current_cycle):
                        self.timing_checker.read(req.bank, current_cycle)
                        self.completion_cycle = current_cycle + CONFIG.READ_LATENCY
                        self.current_stage = "READING"
                elif req.operation == RequestType.WRITE:
                    if self.timing_checker.can_write(req.bank, current_cycle):
                        self.timing_checker.write(req.bank, current_cycle)
                        self.completion_cycle = current_cycle + CONFIG.WRITE_LATENCY
                        self.current_stage = "WRITING"

    def is_idle(self) -> bool:
        """
        Check if the memory controller is completely idle.

        Returns:
            True if there is no active request and the scheduler is empty.
        """
        return self.current_request is None and self.scheduler.queue_length() == 0
