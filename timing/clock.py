"""
Global simulation clock.
"""


class Clock:

    def __init__(self):
        self.cycle = 0

    def tick(self):
        """Advance one clock cycle."""
        self.cycle += 1

    def reset(self):
        self.cycle = 0

    def now(self):
        return self.cycle

    def __repr__(self):
        return f"Clock(cycle={self.cycle})"