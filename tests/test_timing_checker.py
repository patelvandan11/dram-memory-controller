import unittest

from timing.timing_checker import TimingChecker
from timing.clock import Clock


class TestTimingChecker(unittest.TestCase):

    def test_trcd(self):
        clock = Clock()
        timing = TimingChecker()

        bank = 0

        timing.activate(bank, clock.now())

        self.assertFalse(
            timing.can_read(bank, clock.now())
        )

        for _ in range(18):
            clock.tick()

        self.assertTrue(
            timing.can_read(bank, clock.now())
        )

    def test_tras(self):
        clock = Clock()
        timing = TimingChecker()

        bank = 0

        timing.activate(bank, clock.now())

        self.assertFalse(
            timing.can_precharge(bank, clock.now())
        )

        for _ in range(42):
            clock.tick()

        self.assertTrue(
            timing.can_precharge(bank, clock.now())
        )


if __name__ == "__main__":
    unittest.main()