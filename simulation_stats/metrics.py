# metrics.py

"""
Statistics module for the DRAM Memory Controller Simulator.
"""

from __future__ import annotations

import csv
from dataclasses import dataclass, field
from pathlib import Path


@dataclass
class Metrics:
    """
    Collects and reports simulation statistics.
    """

    total_requests: int = 0
    completed_requests: int = 0

    total_latency: int = 0
    maximum_latency: int = 0
    minimum_latency: int = field(default_factory=lambda: float("inf"))

    read_requests: int = 0
    write_requests: int = 0

    transferred_bytes: int = 0

    simulation_cycles: int = 0

    latencies: list[int] = field(default_factory=list)
    bank_utilization: dict[int, int] = field(default_factory=dict)

    def record_bank_access(self, bank_id: int) -> None:
        """Record an access to a DRAM bank."""
        self.bank_utilization[bank_id] = self.bank_utilization.get(bank_id, 0) + 1

    def print_summary(self) -> None:
        """Print a summary of the metrics to the console."""
        print("\n" + "=" * 40)
        print("      SIMULATION METRICS SUMMARY")
        print("=" * 40)
        print(f"Total Requests:         {self.total_requests}")
        print(f"Completed Requests:     {self.completed_requests}")
        print(f"Simulation Cycles:      {self.simulation_cycles}")
        print(f"Average Latency:        {self.average_latency():.2f} cycles")
        print(f"Maximum Latency:        {self.maximum_latency} cycles")
        min_lat = 0 if self.minimum_latency == float("inf") else self.minimum_latency
        print(f"Minimum Latency:        {min_lat} cycles")
        print(f"Throughput:             {self.throughput():.4f} requests/cycle")
        print(f"Bandwidth:              {self.bandwidth():.2f} bytes/cycle")
        print(f"Read Requests:          {self.read_requests}")
        print(f"Write Requests:         {self.write_requests}")
        print(f"Read/Write Ratio:       {self.read_write_ratio():.2f}")
        print("=" * 40 + "\n")

    def record_request(self, is_read: bool) -> None:
        """
        Record a newly submitted request.

        Args:
            is_read: True if the request is a READ operation,
                     False for WRITE.
        """
        self.total_requests += 1

        if is_read:
            self.read_requests += 1
        else:
            self.write_requests += 1

    def record_completion(
        self,
        latency: int,
        bytes_transferred: int = 64,
    ) -> None:
        """
        Record a completed memory request.

        Args:
            latency:
                Request latency in clock cycles.

            bytes_transferred:
                Bytes transferred for this request.
                Default = 64-byte cache line.
        """

        self.completed_requests += 1

        self.total_latency += latency
        self.latencies.append(latency)

        self.maximum_latency = max(
            self.maximum_latency,
            latency,
        )

        self.minimum_latency = min(
            self.minimum_latency,
            latency,
        )

        self.transferred_bytes += bytes_transferred

    def average_latency(self) -> float:
        """
        Average request latency.
        """

        if self.completed_requests == 0:
            return 0.0

        return self.total_latency / self.completed_requests

    def throughput(self) -> float:
        """
        Requests completed per simulation cycle.
        """

        if self.simulation_cycles == 0:
            return 0.0

        return (
            self.completed_requests /
            self.simulation_cycles
        )

    def bandwidth(self) -> float:
        """
        Bytes transferred per simulation cycle.
        """

        if self.simulation_cycles == 0:
            return 0.0

        return (
            self.transferred_bytes /
            self.simulation_cycles
        )

    def read_write_ratio(self) -> float:
        """
        READ / WRITE ratio.
        """

        if self.write_requests == 0:

            if self.read_requests == 0:
                return 0.0

            return float("inf")

        return (
            self.read_requests /
            self.write_requests
        )

    def export_csv(
        self,
        filename: str = "simulation_statistics.csv",
    ) -> None:
        """
        Export statistics to CSV.
        """

        path = Path(filename)

        with path.open(
            mode="w",
            newline="",
            encoding="utf-8",
        ) as file:

            writer = csv.writer(file)

            writer.writerow(["Metric", "Value"])

            writer.writerow(
                ["Total Requests", self.total_requests]
            )

            writer.writerow(
                ["Completed Requests",
                 self.completed_requests]
            )

            writer.writerow(
                ["Average Latency",
                 self.average_latency()]
            )

            writer.writerow(
                ["Maximum Latency",
                 self.maximum_latency]
            )

            writer.writerow(
                [
                    "Minimum Latency",
                    0
                    if self.minimum_latency == float("inf")
                    else self.minimum_latency,
                ]
            )

            writer.writerow(
                ["Throughput",
                 self.throughput()]
            )

            writer.writerow(
                ["Bandwidth (Bytes/Cycle)",
                 self.bandwidth()]
            )

            writer.writerow(
                ["Read Requests",
                 self.read_requests]
            )

            writer.writerow(
                ["Write Requests",
                 self.write_requests]
            )

            writer.writerow(
                ["Read/Write Ratio",
                 self.read_write_ratio()]
            )