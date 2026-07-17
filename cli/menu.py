"""
CLI Interactive Menu Module
===========================

Provides a text-based interactive menu for loading traces, running simulations,
viewing statistics, generating graphs, and exporting CSV files.
"""

import os
from typing import List, Optional, Dict
from memory_requests.csv_loader import CSVLoader
from simulation.simulation_engine import SimulationEngine
from simulation_stats.metrics import Metrics
from visualization.plotter import Plotter


class MenuState:
    """Tracks state across menu options."""
    def __init__(self):
        self.trace_file: str = "requests.csv"
        self.fcfs_metrics: Optional[Metrics] = None
        self.frfcfs_metrics: Optional[Metrics] = None
        self.active_metrics: Optional[Metrics] = None
        self.active_scheduler: str = "FCFS"


def print_comparison_table(fcfs: Metrics, frfcfs: Metrics) -> None:
    """Print a side-by-side performance comparison table."""
    print("\n" + "=" * 70)
    print("                SCHEDULER PERFORMANCE COMPARISON")
    print("=" * 70)
    print(f"{'Metric':<25} | {'FCFS':<15} | {'FR-FCFS':<15} | {'Improvement':<12}")
    print("-" * 70)

    # 1. Total Requests
    print(f"{'Total Requests':<25} | {fcfs.total_requests:<15} | {frfcfs.total_requests:<15} | {'-':<12}")

    # 2. Completed Requests
    print(f"{'Completed Requests':<25} | {fcfs.completed_requests:<15} | {frfcfs.completed_requests:<15} | {'-':<12}")

    # 3. Simulation Cycles
    cycles_imp = ((fcfs.simulation_cycles - frfcfs.simulation_cycles) / fcfs.simulation_cycles * 100) if fcfs.simulation_cycles else 0.0
    print(f"{'Simulation Cycles':<25} | {fcfs.simulation_cycles:<15} | {frfcfs.simulation_cycles:<15} | {cycles_imp:.1f}% lower")

    # 4. Average Latency
    fcfs_lat = fcfs.average_latency()
    frfcfs_lat = frfcfs.average_latency()
    lat_imp = ((fcfs_lat - frfcfs_lat) / fcfs_lat * 100) if fcfs_lat else 0.0
    print(f"{'Average Latency':<25} | {fcfs_lat:<12.1f} cyc | {frfcfs_lat:<12.1f} cyc | {lat_imp:.1f}% lower")

    # 5. Maximum Latency
    fcfs_max = fcfs.maximum_latency
    frfcfs_max = frfcfs.maximum_latency
    max_imp = ((fcfs_max - frfcfs_max) / fcfs_max * 100) if fcfs_max else 0.0
    print(f"{'Maximum Latency':<25} | {fcfs_max:<12} cyc | {frfcfs_max:<12} cyc | {max_imp:.1f}% lower")

    # 6. Throughput
    fcfs_th = fcfs.throughput()
    frfcfs_th = frfcfs.throughput()
    th_imp = ((frfcfs_th - fcfs_th) / fcfs_th * 100) if fcfs_th else 0.0
    print(f"{'Throughput':<25} | {fcfs_th:<12.4f} req/c| {frfcfs_th:<12.4f} req/c| {th_imp:.1f}% higher")

    # 7. Bandwidth
    fcfs_bw = fcfs.bandwidth()
    frfcfs_bw = frfcfs.bandwidth()
    bw_imp = ((frfcfs_bw - fcfs_bw) / fcfs_bw * 100) if fcfs_bw else 0.0
    print(f"{'Bandwidth':<25} | {fcfs_bw:<12.2f} B/c  | {frfcfs_bw:<12.2f} B/c  | {bw_imp:.1f}% higher")

    print("=" * 70 + "\n")


def run_menu():
    state = MenuState()

    while True:
        print("\n====================================")
        print(" DRAM Memory Controller Simulator")
        print("====================================")
        print(f"Current Trace File: {state.trace_file}")
        print("------------------------------------")
        print("1. Set / Load Trace File")
        print("2. Run FCFS Simulation")
        print("3. Run FR-FCFS Simulation")
        print("4. Run Both & Compare Performance")
        print("5. Show Last Run Statistics")
        print("6. Generate / Save Graphs")
        print("7. Export CSV Statistics")
        print("8. Exit")

        choice = input("\nSelect option: ").strip()

        if choice == "1":
            file_path = input("Enter path to trace CSV file [default: requests.csv]: ").strip()
            if not file_path:
                file_path = "requests.csv"
            
            if not os.path.exists(file_path):
                print(f"Error: File '{file_path}' does not exist.")
            else:
                state.trace_file = file_path
                try:
                    loader = CSVLoader()
                    reqs = loader.load(file_path)
                    print(f"Successfully loaded trace file with {len(reqs)} memory requests.")
                except Exception as e:
                    print(f"Error loading trace file: {e}")

        elif choice in ("2", "3", "4"):
            if not os.path.exists(state.trace_file):
                print(f"Error: Trace file '{state.trace_file}' not found. Please set it using Option 1.")
                continue

            print(f"Starting simulation on '{state.trace_file}'...")
            
            if choice == "2":
                engine = SimulationEngine(state.trace_file, "fcfs")
                state.fcfs_metrics = engine.run()
                state.active_metrics = state.fcfs_metrics
                state.active_scheduler = "FCFS"
                print("FCFS simulation complete.")
                state.active_metrics.print_summary()

            elif choice == "3":
                engine = SimulationEngine(state.trace_file, "frfcfs")
                state.frfcfs_metrics = engine.run()
                state.active_metrics = state.frfcfs_metrics
                state.active_scheduler = "FR-FCFS"
                print("FR-FCFS simulation complete.")
                state.active_metrics.print_summary()

            elif choice == "4":
                # FCFS Run
                print("Running FCFS...")
                engine_fcfs = SimulationEngine(state.trace_file, "fcfs")
                state.fcfs_metrics = engine_fcfs.run()

                # FR-FCFS Run
                print("Running FR-FCFS...")
                engine_frfc = SimulationEngine(state.trace_file, "frfcfs")
                state.frfcfs_metrics = engine_frfc.run()

                state.active_metrics = state.frfcfs_metrics
                state.active_scheduler = "FR-FCFS"

                print("Both simulations complete.")
                print_comparison_table(state.fcfs_metrics, state.frfcfs_metrics)

        elif choice == "5":
            if state.active_metrics is None:
                print("No simulation has been run yet. Please run a simulation first (Options 2, 3, or 4).")
            else:
                print(f"Showing statistics for last run ({state.active_scheduler}):")
                state.active_metrics.print_summary()

        elif choice == "6":
            if state.active_metrics is None:
                print("No simulation data available. Please run a simulation first.")
            else:
                print("Generating graphs...")
                try:
                    plotter = Plotter(state.active_metrics)
                    plotter.plot_latency()
                    plotter.plot_throughput()
                    plotter.plot_bank_utilization()
                    print("Graphs generated successfully and saved to 'graphs/' directory.")
                except Exception as e:
                    print(f"Error generating graphs: {e}")

        elif choice == "7":
            if state.active_metrics is None:
                print("No simulation data available. Please run a simulation first.")
            else:
                print("Exporting statistics to CSV...")
                try:
                    state.active_metrics.export_csv("simulation_statistics.csv")
                    print("Successfully exported statistics to 'simulation_statistics.csv'.")
                except Exception as e:
                    print(f"Error exporting CSV: {e}")

        elif choice == "8":
            print("Goodbye!")
            break

        else:
            print("Invalid option. Please enter 1-8.")