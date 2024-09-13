#!/usr/bin/env python3

import argparse
import logging
import sys
import os
from pathlib import Path

import qiskit

from icsystemutils.monitor import Profiler
from icplot.graph import Plot
from icplot.color import Color
from ictasks.tasks import TaskCollection

from icquantum.session import QuantumCircuitBenchmarkSession
from icquantum.simulation import QuantumSimulation
from icquantum.circuit_cache import QuantumCircuitCache
from icquantum.plot import PlotGenerator
from icquantum.qiskit import setup_aer_backend


logger = logging.getLogger(__name__)


def benchmark(args):
    simulation = QuantumSimulation()
    simulation.circuit_label = args.circuit
    simulation.num_qubits = args.num_qubits
    simulation.num_iters = args.num_iters
    simulation.num_circuits = args.num_circuits
    simulation.backend.library = "qiskit_aer"
    simulation.backend.library_version = qiskit.version.get_version_info()
    simulation.backend.num_cores = args.num_cores
    simulation.backend.num_parallel_exp = args.num_parallel_exp
    simulation.backend.parallel_threshold = args.parallelization_threshold
    simulation.backend.use_gpu = args.use_gpu
    simulation.backend.library_backend = "statevector_simulator"

    backend = setup_aer_backend(simulation.backend)

    circuits = QuantumCircuitCache()

    profilers = []
    if args.do_profile:
        profilers.append(Profiler())

    session = QuantumCircuitBenchmarkSession(backend, circuits, profilers)
    try:
        session.run(simulation, work_dir=args.work_dir.resolve())
    except RuntimeError as e:
        logger.error("Exception while running session: %s", e)
        sys.exit(1)


def postprocess(args):

    plots = {
        "runtime": Plot(
            title="Circuit Simulation Time vs. Number of Qubits",
            x_label="Number of Qubits",
            y_label="Runtime (s)",
            legend_label="circuit",
        ),
    }

    colormap = {"sample": Color()}

    tasks = TaskCollection(args.result_dir.resolve())

    plot_generator = PlotGenerator(
        tasks,
        plots,
        colormap,
        "circuit_label",
        "num_qubits",
        "quantum_simulation.json",
        args.result_dir.resolve(),
    )
    plot_generator.make_plots()


def main_cli():

    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(required=True)

    benchmark_parser = subparsers.add_parser("benchmark")

    benchmark_parser.add_argument(
        "--work_dir",
        type=Path,
        default=Path(os.getcwd()),
        help="Directory for writing results to",
    )
    benchmark_parser.add_argument(
        "--num_qubits", type=int, default=5, help="Number of qubits in the circuit"
    )
    benchmark_parser.add_argument(
        "--num_circuits",
        type=int,
        default=1,
        help="Number of copies of the circuit to send to the backend",
    )
    benchmark_parser.add_argument(
        "--num_iters",
        type=int,
        default=1,
        help="Number of times to repeat the analysis",
    )
    benchmark_parser.add_argument(
        "--num_cores",
        type=int,
        default=0,
        help="Number of cores to use, default of 0 uses all available cores",
    )
    benchmark_parser.add_argument(
        "--num_parallel_exp",
        type=int,
        default=1,
        help="Number of experiments to run in parallel in qiskit",
    )
    benchmark_parser.add_argument(
        "--parallelization_threshold",
        type=int,
        default=14,
        help=("Number of Qubits at which to parallelise" " individual circuits"),
    )
    benchmark_parser.add_argument(
        "--profile",
        action="store_true",
        dest="do_profile",
        default=False,
        help="Enables profiling with cProfile",
    )
    benchmark_parser.add_argument(
        "--use_gpu",
        action="store_true",
        dest="use_gpu",
        default=False,
        help="Enables GPU acceleration",
    )
    benchmark_parser.add_argument(
        "--circuit",
        type=str,
        default="sample",
        help="Pick a circuit from mqtbench using this label",
    )
    benchmark_parser.set_defaults(func=benchmark)

    benchmarkpp_parser = subparsers.add_parser("benchmark_postprocess")
    benchmarkpp_parser.add_argument(
        "--result_dir",
        type=Path,
        required=True,
        help="The path to directory to be searched.",
    )

    benchmarkpp_parser.set_defaults(func=postprocess)

    args = parser.parse_args()
    fmt = "%(asctime)s%(msecs)03d | %(filename)s:%(lineno)s:%(funcName)s | %(message)s"
    logging.basicConfig(
        format=fmt,
        datefmt="%Y%m%dT%H:%M:%S:",
        level=logging.INFO,
    )

    args.func(args)


if __name__ == "__main__":
    main_cli()
