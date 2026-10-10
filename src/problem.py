import numpy as np
from qiskit import QuantumCircuit

def create_knapsack_logical_circuit(values, weights, max_capacity, penalty_factor=10):
    num_items = len(values)
    qc = QuantumCircuit(num_items)
    for i in range(num_items):
        qc.h(i)
    for i, val in enumerate(values):
        qc.rz(-val * 0.1, i)
    for i in range(num_items):
        for j in range(i + 1, num_items):
            joint_penalty = penalty_factor * weights[i] * weights[j] * 0.05
            qc.cx(i, j)
            qc.rz(joint_penalty, j)
            qc.cx(i, j)
    return qc
