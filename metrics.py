from simulation_stats.metrics import Metrics

stats = Metrics()

stats.simulation_cycles = 100

stats.record_request(True)
stats.record_request(False)
stats.record_request(True)

stats.record_completion(18)
stats.record_completion(25)
stats.record_completion(20)

print(stats.average_latency())
print(stats.throughput())
print(stats.bandwidth())
print(stats.read_write_ratio())

stats.export_csv()