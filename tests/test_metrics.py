# test_metrics.py

import os
import tempfile
import unittest

from simulation_stats.metrics import Metrics


class TestMetrics(unittest.TestCase):

    def test_request_count(self):
        stats = Metrics()

        stats.record_request(True)
        stats.record_request(False)

        self.assertEqual(stats.total_requests, 2)
        self.assertEqual(stats.read_requests, 1)
        self.assertEqual(stats.write_requests, 1)

    def test_latency(self):
        stats = Metrics()

        stats.record_completion(20)
        stats.record_completion(30)
        stats.record_completion(10)

        self.assertEqual(stats.maximum_latency, 30)
        self.assertEqual(stats.minimum_latency, 10)
        self.assertEqual(stats.average_latency(), 20)

    def test_throughput(self):
        stats = Metrics()

        stats.simulation_cycles = 100

        stats.record_completion(10)
        stats.record_completion(20)

        self.assertAlmostEqual(
            stats.throughput(),
            0.02,
        )

    def test_bandwidth(self):
        stats = Metrics()

        stats.simulation_cycles = 64

        stats.record_completion(10)
        stats.record_completion(10)

        self.assertEqual(
            stats.bandwidth(),
            2.0,
        )

    def test_export_csv(self):
        stats = Metrics()

        stats.record_request(True)
        stats.record_completion(15)

        with tempfile.TemporaryDirectory() as tmpdir:
            path = os.path.join(tmpdir, "stats.csv")
            stats.export_csv(path)
            self.assertTrue(os.path.exists(path))


if __name__ == "__main__":
    unittest.main()