"""
Simulation Engine Module
========================

Coordinates the entire DRAM simulation process, managing the clock, loading trace files,
dispatching requests, and stepping the memory controller.
"""

from typing import List
from controller.scheduler import FCFSScheduler, FRFCFSScheduler, BaseScheduler
from memory_requests.csv_loader import CSVLoader
from memory_requests.memory_request import MemoryRequest
from simulation_stats.metrics import Metrics
from simulation.memory_controller import MemoryController
from timing.clock import Clock


class SimulationEngine:
    """
    Simulation engine for the DRAM memory controller.
    """

    def __init__(self, trace_file: str, scheduler_type: str = "fcfs"):
        """
        Initialize the simulation engine.

        Args:
            trace_file: Path to the memory request CSV file.
            scheduler_type: Type of scheduler to use ("fcfs" or "frfcfs").
        """
        self.trace_file: str = trace_file
        self.scheduler_type: str = scheduler_type.lower()
        self.clock: Clock = Clock()
        self.metrics: Metrics = Metrics()

        # Select scheduler instance
        if self.scheduler_type == "frfcfs":
            self.scheduler: BaseScheduler = FRFCFSScheduler()
        else:
            self.scheduler: BaseScheduler = FCFSScheduler()

        self.controller: MemoryController = MemoryController(self.scheduler, self.metrics)
        self.loader: CSVLoader = CSVLoader()
        self.requests: List[MemoryRequest] = []

    def run(self) -> Metrics:
        """
        Run the simulation cycle-by-cycle until all requests are completed.

        Returns:
            The collected Metrics object containing simulation statistics.
        """
        # Load requests from CSV file
        self.requests = self.loader.load(self.trace_file)

        # Sort requests by arrival time to dispatch them correctly
        pending_requests = sorted(self.requests, key=lambda r: r.arrival_time)
        active_request_index = 0
        total_requests_count = len(pending_requests)

        self.clock.reset()

        # Run cycle-by-cycle loop
        while active_request_index < total_requests_count or not self.controller.is_idle():
            current_cycle = self.clock.now()

            # 1. Dispatch requests that have arrived at or before the current cycle
            while active_request_index < total_requests_count:
                req = pending_requests[active_request_index]
                if req.arrival_time <= current_cycle:
                    self.controller.add_request(req)
                    active_request_index += 1
                else:
                    # Requests are sorted by arrival time, so if this one hasn't arrived, none of the subsequent ones have either.
                    break

            # 2. Step the memory controller
            self.controller.step(current_cycle)

            # 3. Advance the simulation clock
            self.clock.tick()

        # Record total simulation cycles in the metrics object
        self.metrics.simulation_cycles = self.clock.now()

        return self.metrics
