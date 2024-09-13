import logging
from pathlib import Path


from icsystemutils.monitor import Profiler

from .circuit_cache import QuantumCircuitCache
from .simulation import QuantumSimulation


logger = logging.getLogger(__name__)


class QuantumCircuitBenchmarkSession:
    """
    This session runs batches of quantum circuits
    """

    def __init__(
        self,
        backend,
        circuits: QuantumCircuitCache,
        profilers: list[Profiler] | None = None,
    ):
        self.backend = backend
        if profilers:
            self.profilers = profilers
        else:
            self.profilers = []
        self.circuits = circuits

    def run_circuits(self, circuits):
        logger.info("Running %d circuits", len(circuits))
        job = self.backend.run(circuits)
        job.result()

    def load_circuit(self, circuit_label: str, num_qubits: int):
        try:
            qc = self.circuits.get_circuit(circuit_label, num_qubits)
        except RuntimeError as e:
            logger.error("Failed to load circuits with: %s", e)
            raise e
        return qc

    def run(self, sim: QuantumSimulation, work_dir: Path) -> None:

        logger.info("Starting benchmark")
        sim.write(work_dir)

        logger.info("Loading circuits")
        qc = self.load_circuit(sim.circuit_label, sim.num_qubits)
        qcs = [qc] * sim.num_circuits

        for profiler in self.profilers:
            profiler.start()

        logger.info("Starting simulation")
        sim.on_started()

        for _ in range(sim.num_iters):
            self.run_circuits(qcs)

        sim.on_finished()
        sim.write(work_dir)
        logger.info("Finished simulation")

        for profiler in self.profilers:
            profiler.stop()

        logger.info("Finished benchmark")
