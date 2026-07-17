"""
Visualization Module for DRAM Memory Controller Simulator

Generates:
1. Latency Histogram
2. Throughput Chart
3. Bank Utilization Chart
"""

import os
import matplotlib.pyplot as plt


class Plotter:

    def __init__(self, metrics):

        self.metrics = metrics

        os.makedirs("graphs", exist_ok=True)

    # --------------------------------------------------

    def plot_latency(self):

        latencies = self.metrics.latencies

        if not latencies:
            print("No latency data available.")
            return

        plt.figure(figsize=(8, 5))

        plt.hist(
            latencies,
            bins=10,
            edgecolor="black"
        )

        plt.title("Latency Distribution")
        plt.xlabel("Latency (Cycles)")
        plt.ylabel("Number of Requests")

        plt.grid(True)

        plt.tight_layout()

        plt.savefig("graphs/latency_histogram.png")

        plt.close()

        print("Saved graphs/latency_histogram.png")

    # --------------------------------------------------

    def plot_throughput(self):

        throughput = self.metrics.throughput()

        plt.figure(figsize=(5, 5))

        plt.bar(
            ["Throughput"],
            [throughput]
        )

        plt.ylabel("Requests / Cycle")

        plt.title("Simulation Throughput")

        plt.tight_layout()

        plt.savefig("graphs/throughput.png")

        plt.close()

        print("Saved graphs/throughput.png")

    # --------------------------------------------------

    def plot_bank_utilization(self):

        utilization = self.metrics.bank_utilization

        if not utilization:
            print("No bank utilization data available.")
            return

        banks = list(utilization.keys())

        values = list(utilization.values())

        plt.figure(figsize=(8, 5))

        plt.bar(banks, values)

        plt.xlabel("Bank")

        plt.ylabel("Access Count")

        plt.title("Bank Utilization")

        plt.tight_layout()

        plt.savefig("graphs/bank_utilization.png")

        plt.close()

        print("Saved graphs/bank_utilization.png")