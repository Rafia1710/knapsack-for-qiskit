import json
from qiskit_aer.noise import NoiseModel, depolarizing_error

def load_processor_configuration(json_path):
    with open(json_path, 'r', encoding='utf-8') as f:
        return json.load(f)

def build_noise_model(proc_def):
    noise_model = NoiseModel()
    p1q = proc_def.get("noise", {}).get("gate_error_1q", 0.001)
    p2q = proc_def.get("noise", {}).get("gate_error_2q", 0.01)
    err_1q = depolarizing_error(p1q, 1)
    err_2q = depolarizing_error(p2q, 2)
    noise_model.add_all_qubit_quantum_error(err_1q, ['x', 'sx', 'rz'])
    noise_model.add_all_qubit_quantum_error(err_2q, ['cx'])
    return noise_model
