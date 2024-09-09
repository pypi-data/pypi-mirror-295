import os
from pathlib import Path
import shutil

from icquantum.session import QuantumCircuitBenchmarkSession
from icquantum.simulation import QuantumSimulation
from icquantum.circuit_cache import QuantumCircuitCache
from icquantum.qiskit import setup_aer_backend


def test_benchmarking():

    simulation = QuantumSimulation()
    simulation.circuit_label = "sample"
    simulation.num_qubits = 5
    simulation.num_iters = 3
    simulation.num_circuits = 10
    simulation.backend.library = "qiskit_aer"
    simulation.backend.library_version = "1.2.3"
    simulation.backend.num_cores = 0
    simulation.backend.library_backend = "statevector_simulator"

    backend = setup_aer_backend(simulation.backend)

    circuits = QuantumCircuitCache()

    session = QuantumCircuitBenchmarkSession(backend, circuits)

    work_dir = Path(os.getcwd()) / "test_benchmarking"
    session.run(simulation, work_dir=work_dir)

    shutil.rmtree(work_dir)

