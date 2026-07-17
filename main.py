"""
DRAM Memory Controller Simulator CLI Driver
===========================================

Provides the command line interface to run simulations, show statistics,
generate graphs, export CSV reports, and open the interactive menu.
"""

import argparse
import os
import pickle
import sys
from typing import Dict, Optional

from cli.menu import run_menu, print_comparison_table
from memory_requests.csv_loader import CSVLoader
from simulation.simulation_engine import SimulationEngine
from simulation_stats.metrics import Metrics
from visualization.plotter import Plotter

# Path to serialize simulation results for cross-command persistence
STATE_FILE_PATH = ".simulation_state.pkl"


def build_parser() -> argparse.ArgumentParser:
    """Build the CLI argument parser."""
    parser = argparse.ArgumentParser(
        description="DRAM Memory Controller Simulator"
    )

    subparsers = parser.add_subparsers(dest="command")

    # Menu command
    subparsers.add_parser("menu", help="Launch interactive menu")

    # Stats command
    subparsers.add_parser("stats", help="Show statistics of the last simulation run")

    # Graphs command
    subparsers.add_parser("graphs", help="Generate performance graphs from the last simulation run")

    # Export command
    subparsers.add_parser("export", help="Export statistics of the last run to CSV")

    # Run command
    run = subparsers.add_parser("run", help="Run simulation on a request trace file")
    run.add_argument(
        "--trace",
        required=True,
        help="Path to request trace CSV file"
    )
    run.add_argument(
        "--scheduler",
        choices=["fcfs", "frfcfs", "both"],
        default="both",
        help="Scheduling policy to simulate (default: both and compare)"
    )

    return parser


def save_simulation_state(state: Dict[str, Optional[Metrics]]) -> None:
    """Save simulation metrics to a file for persistence."""
    try:
        with open(STATE_FILE_PATH, "wb") as f:
            pickle.dump(state, f)
    except Exception as e:
        print(f"Warning: Failed to save simulation state: {e}")


def load_simulation_state() -> Optional[Dict[str, Optional[Metrics]]]:
    """Load serialized simulation metrics."""
    if not os.path.exists(STATE_FILE_PATH):
        return None
    try:
        with open(STATE_FILE_PATH, "rb") as f:
            return pickle.load(f)
    except Exception as e:
        print(f"Warning: Failed to load simulation state: {e}")
        return None


def run_simulation(trace_file: str, scheduler_type: str) -> None:
    """Run simulation using the specified scheduler(s)."""
    if not os.path.exists(trace_file):
        print(f"\nERROR: Trace file not found: {trace_file}")
        sys.exit(1)

    print("=" * 60)
    print("DRAM MEMORY CONTROLLER SIMULATOR")
    print("=" * 60)
    print(f"Loading trace: {trace_file}")

    # Validate that we can load the requests
    try:
        loader = CSVLoader()
        reqs = loader.load(trace_file)
        print(f"Successfully loaded {len(reqs)} memory requests.")
    except Exception as e:
        print(f"Error parsing trace file: {e}")
        sys.exit(1)

    state: Dict[str, Optional[Metrics]] = {
        "fcfs": None,
        "frfcfs": None,
        "active": None,
        "active_name": ""
    }

    if scheduler_type in ("fcfs", "both"):
        print("\nRunning FCFS Simulation...")
        engine = SimulationEngine(trace_file, "fcfs")
        state["fcfs"] = engine.run()
        state["active"] = state["fcfs"]
        state["active_name"] = "FCFS"
        print("FCFS Simulation completed.")

    if scheduler_type in ("frfcfs", "both"):
        print("\nRunning FR-FCFS Simulation...")
        engine = SimulationEngine(trace_file, "frfcfs")
        state["frfcfs"] = engine.run()
        state["active"] = state["frfcfs"]
        state["active_name"] = "FR-FCFS"
        print("FR-FCFS Simulation completed.")

    # Save state for other commands to access
    save_simulation_state(state)

    # Show results
    if scheduler_type == "both" and state["fcfs"] is not None and state["frfcfs"] is not None:
        print_comparison_table(state["fcfs"], state["frfcfs"])
        print("Saving performance graphs for FR-FCFS...")
        try:
            plotter = Plotter(state["frfcfs"])
            plotter.plot_latency()
            plotter.plot_throughput()
            plotter.plot_bank_utilization()
        except Exception as e:
            print(f"Warning: Failed to generate graphs: {e}")
            
        print("Exporting FR-FCFS statistics to 'simulation_statistics.csv'...")
        try:
            state["frfcfs"].export_csv("simulation_statistics.csv")
        except Exception as e:
            print(f"Warning: Failed to export CSV: {e}")
    else:
        active_metrics = state["active"]
        active_name = state["active_name"]
        if active_metrics is not None:
            print(f"\nSimulation Results ({active_name}):")
            active_metrics.print_summary()
            
            print(f"Generating graphs for {active_name}...")
            try:
                plotter = Plotter(active_metrics)
                plotter.plot_latency()
                plotter.plot_throughput()
                plotter.plot_bank_utilization()
            except Exception as e:
                print(f"Warning: Failed to generate graphs: {e}")

            print(f"Exporting statistics to 'simulation_statistics.csv'...")
            try:
                active_metrics.export_csv("simulation_statistics.csv")
            except Exception as e:
                print(f"Warning: Failed to export CSV: {e}")


def show_statistics() -> None:
    """Load persisted metrics and print summary or comparison."""
    state = load_simulation_state()
    if state is None:
        print("Error: No simulation results found. Run a simulation first using the 'run' command.")
        return

    if state.get("fcfs") is not None and state.get("frfcfs") is not None:
        print_comparison_table(state["fcfs"], state["frfcfs"])
    elif state.get("active") is not None:
        print(f"\nSimulation Results ({state['active_name']}):")
        state["active"].print_summary()
    else:
        print("Error: Simulated metrics state is corrupt or empty.")


def generate_graphs() -> None:
    """Load persisted metrics and generate plots."""
    state = load_simulation_state()
    if state is None:
        print("Error: No simulation results found. Run a simulation first using the 'run' command.")
        return

    active_metrics = state.get("active")
    active_name = state.get("active_name", "Simulation")
    if active_metrics is not None:
        print(f"Generating graphs for {active_name}...")
        try:
            plotter = Plotter(active_metrics)
            plotter.plot_latency()
            plotter.plot_throughput()
            plotter.plot_bank_utilization()
            print("Graphs generated successfully and saved to 'graphs/' directory.")
        except Exception as e:
            print(f"Error generating graphs: {e}")
    else:
        print("Error: No active simulation data available.")


def export_statistics() -> None:
    """Load persisted metrics and export to CSV."""
    state = load_simulation_state()
    if state is None:
        print("Error: No simulation results found. Run a simulation first using the 'run' command.")
        return

    active_metrics = state.get("active")
    if active_metrics is not None:
        print("Exporting statistics to CSV...")
        try:
            active_metrics.export_csv("simulation_statistics.csv")
            print("Successfully exported to 'simulation_statistics.csv'.")
        except Exception as e:
            print(f"Error exporting CSV: {e}")
    else:
        print("Error: No active simulation data available.")


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()

    if args.command == "menu":
        run_menu()
    elif args.command == "run":
        run_simulation(args.trace, args.scheduler)
    elif args.command == "stats":
        show_statistics()
    elif args.command == "graphs":
        generate_graphs()
    elif args.command == "export":
        export_statistics()
    else:
        parser.print_help()


if __name__ == "__main__":
    main()