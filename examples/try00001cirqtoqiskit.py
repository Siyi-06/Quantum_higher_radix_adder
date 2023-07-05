import cirq
from typing import Tuple
from qiskit import QuantumCircuit, execute, Aer


def main():
    q0 = cirq.LineQubit(1)
    cirq_circuit = cirq.Circuit(
        cirq.H(q0),
        cirq.measure(q0)
    )
    results, qasm_circuit = run_cirq_circuit_on_qiskit(cirq_circuit, (q0,), 'qasm_simulator')

    # Returns counts
    counts = results.get_counts(qasm_circuit)
    print("Total count for 00 and 11 are:", counts)


def run_cirq_circuit_on_qiskit(circuit: 'cirq.Circuit', qubits: Tuple['cirq.Qid', ...], backend: str):
    qasm_output = cirq.QasmOutput((circuit.all_operations()), qubits)
    qasm_circuit = QuantumCircuit().from_qasm_str(str(qasm_output))
    # Execute the circuit qiskit backend
    job = execute(qasm_circuit, Aer.get_backend(backend), shots=1000)
    # Grab results from the job
    return job.result(), qasm_circuit


if __name__ == '__main__':
    main()
