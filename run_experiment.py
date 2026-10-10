import pandas as pd
from src.problem import create_knapsack_logical_circuit
from src.processors import load_processor_configuration, build_noise_model
from src.routing import benchmark_circuit

values = [4, 2, 5, 1, 3]
weights = [3, 1, 4, 2, 2]
capacity = 6

print("[1/4] Constructing Knapsack algorithm target logic...")
logical_qc = create_knapsack_logical_circuit(values, weights, capacity)

print("[2/4] Pulling simulated target topology maps...")
proc_A = load_processor_configuration("processors/processor_A.json")
proc_B = load_processor_configuration("processors/processor_B.json")

print("[3/4] Running controlled transpilation and noisy executions...")
metrics_A, _ = benchmark_circuit(logical_qc, proc_A["coupling_map"], build_noise_model(proc_A), proc_A["basis_gates"])
metrics_B, _ = benchmark_circuit(logical_qc, proc_B["coupling_map"], build_noise_model(proc_B), proc_B["basis_gates"])

print("[4/4] Writing metric results to results/tables/AB_comparison.csv...")
df = pd.DataFrame({
    "Metric": ["Depth", "Total Ops", "CX Count", "SWAP Overhead", "Physical Qubits", "Runtime (s)"],
    "Processor A (Linear)": [metrics_A["depth"], metrics_A["total_ops"], metrics_A["cx_gates"], metrics_A["swap_gates"], metrics_A["physical_qubits"], round(metrics_A["runtime"], 4)],
    "Processor B (T-Shape)": [metrics_B["depth"], metrics_B["total_ops"], metrics_B["cx_gates"], metrics_B["swap_gates"], metrics_B["physical_qubits"], round(metrics_B["runtime"], 4)]
})
df["Difference"] = df["Processor B (T-Shape)"] - df["Processor A (Linear)"]
df.to_csv("results/tables/AB_comparison.csv", index=False)
print("\n=== PHASE 1 HACKATHON BENCHMARK MATRIX METRICS ===")
print(df.to_markdown(index=False))
