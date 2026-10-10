import time
from qiskit import transpile
from qiskit_aer import AerSimulator

def benchmark_circuit(logical_circuit, coupling_map, noise_model, basis_gates, shots=2048):
    compiled_circuit = transpile(
        logical_circuit,
        coupling_map=coupling_map,
        basis_gates=basis_gates,
        optimization_level=1
    )
    ops = compiled_circuit.count_ops()
    metrics = {
        "depth": compiled_circuit.depth(),
        "total_ops": sum(ops.values()),
        "cx_gates": ops.get("cx", 0),
        "swap_gates": ops.get("swap", 0),
        "physical_qubits": compiled_circuit.num_qubits
    }
    backend = AerSimulator(noise_model=noise_model)
    compiled_circuit.measure_all()
    start_time = time.time()
    job = backend.run(compiled_circuit, shots=shots)
    result = job.result()
    metrics["runtime"] = time.time() - start_time
    metrics["counts"] = result.get_counts()
    return metrics, compiled_circuit
