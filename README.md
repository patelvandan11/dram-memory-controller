# DRAM Memory Controller Simulator

A modular and extensible **DRAM Memory Controller Simulator** built in Python that models the behavior of a modern DRAM memory controller, including realistic timing constraints, request scheduling algorithms, memory request processing, and performance analysis.

The project is designed with clean software architecture, making it suitable for learning computer architecture concepts, experimenting with scheduling algorithms, and showcasing system design skills.

---

Modern processors execute millions of memory operations every second. The memory controller is responsible for scheduling these requests while satisfying DRAM timing constraints.

This project simulates how a DRAM controller works by implementing:

- Memory request generation
- Address mapping
- Request queues
- FCFS Scheduling
- FR-FCFS Scheduling
- DRAM timing constraints
- Performance statistics
- CSV trace loading
- Simulation clock
- Command execution
- Performance visualization

The simulator is written with modular components so new scheduling algorithms and timing models can easily be added.

---

# Features

## Memory Requests

- Read requests
- Write requests
- CSV trace loading
- Request validation
- Arrival time simulation

---

## Scheduling Algorithms

### FCFS (First Come First Serve)

Processes requests in arrival order.

### FR-FCFS (First Ready First Come First Serve)

Prioritizes:

- Row Buffer Hits
- Older Requests

This reduces average latency and increases throughput.

---

## DRAM Timing

Supports realistic DRAM timing parameters:

- tRCD
- tRAS
- tRP
- CAS Latency
- Burst Length

Prevents timing violations during simulation.

---

## Performance Metrics

Collects:

- Total Requests
- Completed Requests
- Average Latency
- Minimum Latency
- Maximum Latency
- Throughput
- Bandwidth
- Read/Write Ratio

Exports statistics to CSV.

---

## Command Line Interface

Interactive CLI supports:

- Load Request Trace
- Start Simulation
- View Statistics
- Generate Graphs
- Export Results

---

## Visualization

Generate graphs including:

- Latency Histogram
- Throughput
- Queue Occupancy
- Bank Utilization
- Request Timeline

---

# DRAM Architecture

```
                CPU
                 │
                 ▼
        Memory Controller
                 │
        ┌────────┴────────┐
        │                 │
        ▼                 ▼
   Request Queue      Scheduler
                           │
             ┌─────────────┴─────────────┐
             │                           │
          FCFS                    FR-FCFS
             │
             ▼
       Timing Checker
             │
             ▼
      Command Generator
             │
             ▼
          DRAM Banks
             │
             ▼
         Statistics
             │
             ▼
        Visualization
```

---

# Project Architecture

```
                    +----------------------+
                    |       CPU            |
                    +----------+-----------+
                               |
                               |
                    Memory Requests
                               |
                               ▼
                +--------------------------+
                |      CSV Loader          |
                +--------------------------+
                               |
                               ▼
                +--------------------------+
                |      Request Queue       |
                +--------------------------+
                               |
                               ▼
                +--------------------------+
                |       Scheduler          |
                +--------------------------+
                 FCFS          FR-FCFS
                               |
                               ▼
                +--------------------------+
                |    Timing Checker        |
                +--------------------------+
                               |
                               ▼
                +--------------------------+
                |  Memory Controller       |
                +--------------------------+
                               |
                               ▼
                +--------------------------+
                |      DRAM Banks          |
                +--------------------------+
                               |
                               ▼
                +--------------------------+
                |      Statistics          |
                +--------------------------+
                               |
                               ▼
                +--------------------------+
                |     Visualization        |
                +--------------------------+
```

---

# Folder Structure

```
dram-memory-controller/
│
├── cli/
│   ├── cli.py
│   └── menu.py
│
├── config/
│   ├── config.py
│   └── dram_config.py
│
├── controller/
│   └── scheduler.py
│
├── memory_requests/
│   ├── csv_loader.py
│   ├── memory_request.py
│   └── request_queue.py
│
├── simulation/
│   ├── dram_bank.py
│   ├── memory_controller.py
│   └── simulation_engine.py
│
├── simulation_stats/
│   └── metrics.py
│
├── timing/
│   ├── clock.py
│   └── timing_checker.py
│
├── visualization/
│   └── plotter.py
│
├── utils/
│   ├── enums.py
│   └── logger.py
│
├── tests/
│   ├── conftest.py
│   ├── test_config.py
│   ├── test_csv_loader.py
│   ├── test_frfcfs_scheduler.py
│   ├── test_integration.py
│   ├── test_memory_request.py
│   ├── test_metrics.py
│   ├── test_performance.py
│   ├── test_request_queue.py
│   ├── test_scheduler.py
│   └── test_timing_checker.py
│
├── main.py
│
├── README.md
│
└── requirements.txt
```

---

# Technologies Used

- Python 3.12+
- Dataclasses
- CSV
- Logging
- Matplotlib
- Pytest
- unittest

---

# Installation

Clone repository

```bash
git clone https://github.com/yourusername/dram-memory-controller.git
```

Move into project

```bash
cd dram-memory-controller
```

Create virtual environment

```bash
python -m venv venv
```

Activate

Windows

```bash
venv\Scripts\activate
```

Linux

```bash
source venv/bin/activate
```

Install dependencies

```bash
pip install -r requirements.txt
```

---

# Running the Simulator

Run interactive menu

```bash
python main.py menu
```

Run simulation

```bash
python main.py run --trace requests.csv
```

View statistics

```bash
python main.py stats
```

Generate graphs

```bash
python main.py graphs
```

Export CSV

```bash
python main.py export
```

---

# Running Tests

Run all tests

```bash
pytest
```

Run with coverage

```bash
pytest --cov=. --cov-report=html
```

Generate HTML report

```
htmlcov/index.html
```

---

# Example CSV Input

```csv
RequestID,Operation,Address,ArrivalTime
1,READ,0x1000,0
2,WRITE,0x3000,4
3,READ,4096,7
4,WRITE,8192,10
```

# Example Output

```
============================================================
DRAM MEMORY CONTROLLER SIMULATOR
============================================================
Loading trace: requests.csv
Successfully loaded 4 memory requests.

Running FCFS Simulation...
FCFS Simulation completed.

Running FR-FCFS Simulation...
FR-FCFS Simulation completed.

======================================================================
                SCHEDULER PERFORMANCE COMPARISON
======================================================================
Metric                    | FCFS            | FR-FCFS         | Improvement 
----------------------------------------------------------------------
Total Requests            | 4               | 4               | -           
Completed Requests        | 4               | 4               | -           
Simulation Cycles         | 211             | 103             | 51.2% lower
Average Latency           | 116.2        cyc | 62.2         cyc | 46.5% lower
Maximum Latency           | 202          cyc | 94           cyc | 53.5% lower
Throughput                | 0.0190       req/c| 0.0388       req/c| 104.9% higher
Bandwidth                 | 1.21         B/c  | 2.49         B/c  | 104.9% higher
======================================================================

Saving performance graphs for FR-FCFS...
Saved graphs/latency_histogram.png
Saved graphs/throughput.png
Saved graphs/bank_utilization.png
Exporting FR-FCFS statistics to 'simulation_statistics.csv'...
```

---

# Screenshots

## Main Menu

```
+-----------------------------------+

 DRAM MEMORY CONTROLLER SIMULATOR

+-----------------------------------+

1 Load Requests

2 Start Simulation

3 Statistics

4 Graphs

5 Export CSV

6 Exit
```

---

## Latency Histogram

```
Insert Screenshot Here

graphs/latency_histogram.png
```

---

## Throughput Graph

```
Insert Screenshot Here

graphs/throughput.png
```

---

## Queue Occupancy

```
Insert Screenshot Here

graphs/queue.png
```

---

## Bank Utilization

```
Insert Screenshot Here

graphs/bank_utilization.png
```

---

# Implemented Algorithms

## Scheduling

- FCFS
- FR-FCFS

---

## DRAM Timing

- tRCD
- tRAS
- tRP
- CAS Latency
- Burst Length

---

## Statistics

- Average Latency
- Throughput
- Bandwidth
- Read/Write Ratio

---

# Future Improvements

Planned enhancements include:

- Full DDR4 timing model
- DDR5 support
- Multi-channel memory
- Multi-rank memory
- Bank Groups
- Refresh Operations
- Write Buffer
- Read/Write Reordering
- Open Page Policy
- Close Page Policy
- Out-of-Order Scheduling
- Power Consumption Model
- Thermal Model
- Multi-core CPU Simulation
- Gantt Chart Visualization
- Real Memory Trace Support
- GUI Dashboard
- Performance Benchmark Suite
- CI/CD Pipeline
- Docker Support

---

# Learning Outcomes

This project demonstrates practical understanding of:

- Computer Architecture
- Operating Systems
- Memory Hierarchy
- DRAM Organization
- Scheduling Algorithms
- Performance Analysis
- Software Design
- Python Programming
- Unit Testing
- Simulation Design

---

# Resume Description

### Short Version

> Developed a modular DRAM Memory Controller Simulator in Python implementing FCFS and FR-FCFS scheduling, realistic DRAM timing constraints (tRCD, tRAS, tRP, CAS Latency), request trace processing, performance statistics, and visualization for memory-system analysis.

---

### Detailed Version

> Designed and implemented a professional DRAM Memory Controller Simulator using Python with a modular architecture. Developed request queues, CSV trace loader, FCFS and FR-FCFS scheduling algorithms, realistic DRAM timing validation, simulation clock, configurable memory parameters, performance metrics, and visualization tools. Built comprehensive unit tests with high code coverage and designed the project following scalable software engineering principles.

---

# License

This project is released under the MIT License.

---

# Author

**Vandan Patel**

B.Tech – Artificial Intelligence & Data Science

GitHub: https://github.com/patelvandan11

---

## Acknowledgements

Inspired by academic and industry DRAM simulators such as:

- Ramulator
- DRAMSim2
- DRAMSim3
- USIMM

These projects provided architectural inspiration while this simulator was implemented independently in Python for educational and research purposes.