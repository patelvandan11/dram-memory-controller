"""
Checks whether DRAM commands satisfy timing constraints.
"""

from config.config import CONFIG


class TimingChecker:

    def __init__(self):

        self.last_activate = {}
        self.last_read = {}
        self.last_write = {}
        self.last_precharge = {}

    # ---------------------------------------------

    def can_activate(self, bank, cycle):

        last = self.last_precharge.get(bank)

        if last is None:
            return True

        return cycle >= last + CONFIG.TRP

    # ---------------------------------------------

    def can_read(self, bank, cycle):

        last = self.last_activate.get(bank)

        if last is None:
            return False

        return cycle >= last + CONFIG.TRCD

    # ---------------------------------------------

    def can_write(self, bank, cycle):

        last = self.last_activate.get(bank)

        if last is None:
            return False

        return cycle >= last + CONFIG.TRCD

    # ---------------------------------------------

    def can_precharge(self, bank, cycle):

        last = self.last_activate.get(bank)

        if last is None:
            return False

        return cycle >= last + CONFIG.TRAS

    # ---------------------------------------------

    def activate(self, bank, cycle):

        self.last_activate[bank] = cycle

    def read(self, bank, cycle):

        self.last_read[bank] = cycle

    def write(self, bank, cycle):

        self.last_write[bank] = cycle

    def precharge(self, bank, cycle):

        self.last_precharge[bank] = cycle