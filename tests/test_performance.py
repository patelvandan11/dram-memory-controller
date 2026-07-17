"""
Performance tests comparing FCFS and FR-FCFS.
"""

import os
import tempfile
import unittest
from simulation.simulation_engine import SimulationEngine


class TestSimulationPerformance(unittest.TestCase):
    """Compares performance of schedulers on workloads with row locality."""

    def setUp(self) -> None:
        # Create a trace with high row buffer hits (locality)
        # Bank 0, Row 5 contains multiple accesses back-to-back
        # 0x1400 maps to: column=0, row=5, bank=0
        # 0x1408 maps to: column=8, row=5, bank=0
        # 0x1410 maps to: column=16, row=5, bank=0
        # 0x1418 maps to: column=24, row=5, bank=0
        # Under FR-FCFS, these row hits should be prioritized
        self.trace_data = (
            "RequestID,Operation,Address,ArrivalTime\n"
            "1,READ,0x1400,0\n"   # Row 5
            "2,READ,0x2000,1\n"   # Row 8
            "3,READ,0x1408,2\n"   # Row 5 (Hit!)
            "4,READ,0x1410,3\n"   # Row 5 (Hit!)
        )
        with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".csv", newline="") as temp:
            temp.write(self.trace_data)
            self.trace_path = temp.name

    def tearDown(self) -> None:
        if os.path.exists(self.trace_path):
            os.remove(self.trace_path)

    def test_scheduling_perf_comparison(self) -> None:
        fcfs_engine = SimulationEngine(self.trace_path, "fcfs")
        fcfs_metrics = fcfs_engine.run()

        frfcfs_engine = SimulationEngine(self.trace_path, "frfcfs")
        frfcfs_metrics = frfcfs_engine.run()

        # Print metrics to check
        print(f"\n[Perf Test] FCFS Cycles: {fcfs_metrics.simulation_cycles}")
        print(f"[Perf Test] FR-FCFS Cycles: {frfcfs_metrics.simulation_cycles}")

        # FR-FCFS must complete in fewer cycles than FCFS due to row hits prioritization
        self.assertLess(
            frfcfs_metrics.simulation_cycles,
            fcfs_metrics.simulation_cycles,
            "FR-FCFS should execute trace with row-locality in fewer cycles than FCFS."
        )

        # Average latency of FR-FCFS must be lower
        self.assertLess(
            frfcfs_metrics.average_latency(),
            fcfs_metrics.average_latency(),
            "FR-FCFS should achieve lower average latency on row-locality workloads."
        )


if __name__ == "__main__":
    unittest.main()
