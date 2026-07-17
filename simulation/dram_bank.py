"""
DRAM Bank Module
================

Represents an individual bank in the DRAM memory system, tracking its open row state.
"""

from typing import Optional


class DRAMBank:
    """
    Represents a DRAM bank.
    
    A bank has rows and columns, and a row buffer that holds the currently open row.
    Only one row in a bank can be open (active) at any given time.
    """

    def __init__(self, bank_id: int):
        """
        Initialize the DRAM bank.

        Args:
            bank_id: The unique identifier for this bank.
        """
        self.bank_id: int = bank_id
        self.open_row: Optional[int] = None  # None indicates the bank is precharged (closed)

    def activate(self, row: int) -> None:
        """
        Open a specific row in this bank.

        Args:
            row: The row index to open.
        """
        self.open_row = row

    def precharge(self) -> None:
        """
        Close the currently open row in this bank (precharge).
        """
        self.open_row = None

    def is_row_open(self, row: int) -> bool:
        """
        Check if the given row is currently open in this bank.

        Args:
            row: The row index to check.
        """
        return self.open_row == row

    def __repr__(self) -> str:
        return f"DRAMBank(id={self.bank_id}, open_row={self.open_row})"
