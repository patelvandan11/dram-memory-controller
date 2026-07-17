from timing.clock import Clock
from timing.timing_checker import TimingChecker

clock = Clock()
timing = TimingChecker()

bank = 0

print(timing.can_activate(bank, clock.now()))

timing.activate(bank, clock.now())

clock.tick()

print(timing.can_read(bank, clock.now()))

for _ in range(18):
    clock.tick()

print(timing.can_read(bank, clock.now()))