"""
Configuration values for the DRAM Memory Controller Simulator.
"""


class DRAMConfig:
    """Stores global DRAM configuration parameters."""

    CHANNELS = 1
    RANKS = 1
    BANK_GROUPS = 4
    BANKS_PER_GROUP = 4

    ROWS = 32768
    COLUMNS = 1024

    CLOCK_FREQUENCY_MHZ = 1600