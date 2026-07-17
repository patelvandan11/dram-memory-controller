"""
DRAM Configuration Module
=========================

This module contains all configurable hardware parameters used by the
DRAM Memory Controller Simulator.

Changing any value here automatically updates the simulator without
modifying the controller or timing logic.
"""

from dataclasses import dataclass


@dataclass(frozen=True)
class DRAMConfig:
    """
    Global DRAM configuration parameters.
    All timing values are expressed in clock cycles unless otherwise noted.
    """

    # ==========================================================
    # Memory Organization
    # ==========================================================

    #: Number of independent memory banks.
    NUM_BANKS: int = 16

    #: Number of rows per bank.
    ROW_SIZE: int = 16384

    #: Number of columns per row.
    COLUMN_SIZE: int = 1024

    # ==========================================================
    # Timing Parameters (Clock Cycles)
    # ==========================================================

    #: READ command latency (tCAS).
    READ_LATENCY: int = 12

    #: WRITE command latency.
    WRITE_LATENCY: int = 12

    #: Row activation delay (tRCD).
    ROW_ACTIVATION_TIME: int = 18

    #: Row precharge delay (tRP).
    PRECHARGE_TIME: int = 18

    # ==========================================================
    # Clock Configuration
    # ==========================================================

    #: DRAM operating frequency in MHz.
    CLOCK_FREQUENCY: int = 1600

    # ==========================================================
    # Derived Parameters
    # ==========================================================
    # ==========================================================
    # DRAM Timing Parameters (Clock Cycles)
    # ==========================================================

    # Activate to Read/Write Delay
    TRCD = 18

    # Minimum Active Time
    TRAS = 42

    # Precharge Time
    TRP = 18

    # CAS Latency
    CAS_LATENCY = 16

    # Burst Length
    BURST_LENGTH = 8
    @property
    def CLOCK_PERIOD_NS(self) -> float:
        """
        Clock period in nanoseconds.

        Formula:
            Period(ns) = 1000 / Frequency(MHz)
        """
        return 1000 / self.CLOCK_FREQUENCY

    @property
    def TOTAL_CELLS(self) -> int:
        """
        Total number of addressable memory cells.
        """
        return (
            self.NUM_BANKS
            * self.ROW_SIZE
            * self.COLUMN_SIZE
        )

    @property
    def MEMORY_SIZE_MB(self) -> float:
        """
        Approximate memory capacity in megabytes
        assuming one byte per memory cell.
        """
        return self.TOTAL_CELLS / (1024 ** 2)


# Global configuration instance
CONFIG = DRAMConfig()

