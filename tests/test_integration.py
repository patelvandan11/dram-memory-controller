"""
Integration tests for the DRAM Memory Controller Simulator.
"""

import os
import tempfile
import unittest
from simulation.simulation_engine import SimulationEngine
from utils.enums import RequestStatus


class TestSimulationIntegration(unittest.TestCase):
    """Verifies end-to-end integration of the simulator components."""

    def setUp(self) -> None:
        # Create a small trace file
        self.trace_data = (
            "RequestID,Operation,Address,ArrivalTime\n"
            "1,READ,0x1000,0\n"
            "2,WRITE,0x2000,2\n"
            "3,READ,4096,5\n"
            "4,WRITE,8192,8\n"
        )
        with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".csv", newline="") as temp:
            temp.write(self.trace_data)
            self.trace_path = temp.name

    def tearDown(self) -> None:
        if os.path.exists(self.trace_path):
            os.remove(self.trace_path)

    def test_fcfs_simulation(self) -> None:
        engine = SimulationEngine(self.trace_path, "fcfs")
        metrics = engine.run()

        # All requests must be completed
        self.assertEqual(metrics.total_requests, 4)
        self.assertEqual(metrics.completed_requests, 4)
        self.assertTrue(metrics.simulation_cycles > 0)
        self.assertEqual(len(metrics.latencies), 4)

        # Check request status
        for req in engine.requests:
            self.assertEqual(req.status, RequestStatus.COMPLETED)
            self.assertIsNotNone(req.start_time)
            self.assertIsNotNone(req.finish_time)
            self.assertEqual(req.latency, req.finish_time - req.arrival_time)

    def test_frfcfs_simulation(self) -> None:
        engine = SimulationEngine(self.trace_path, "frfcfs")
        metrics = engine.run()

        # All requests must be completed
        self.assertEqual(metrics.total_requests, 4)
        self.assertEqual(metrics.completed_requests, 4)
        
        # Verify FR-FCFS operates in fewer cycles due to row buffer hits
        fcfs_engine = SimulationEngine(self.trace_path, "fcfs")
        fcfs_metrics = fcfs_engine.run()
        
        self.assertLess(metrics.simulation_cycles, fcfs_metrics.simulation_cycles)


if __name__ == "__main__":
    unittest.main()
