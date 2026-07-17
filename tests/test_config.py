"""
Unit tests for DRAMConfig.
"""

import unittest
from config.config import CONFIG, DRAMConfig


class TestDRAMConfig(unittest.TestCase):
    """Tests the DRAM config properties and initialization."""

    def test_derived_parameters(self) -> None:
        config = DRAMConfig(
            NUM_BANKS=16,
            ROW_SIZE=16384,
            COLUMN_SIZE=1024,
            CLOCK_FREQUENCY=1600,
        )

        self.assertAlmostEqual(config.CLOCK_PERIOD_NS, 0.625)
        self.assertEqual(config.TOTAL_CELLS, 16 * 16384 * 1024)
        self.assertAlmostEqual(config.MEMORY_SIZE_MB, 256.0)

    def test_global_config_exists(self) -> None:
        self.assertIsNotNone(CONFIG)
        self.assertEqual(CONFIG.NUM_BANKS, 16)


if __name__ == "__main__":
    unittest.main()
