from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator

simulator = AerSimulator()

def quantum_random_bit():
    qc = QuantumCircuit(1, 1)

    # Superposition
    qc.h(0)

    # Measurement
    qc.measure(0, 0)

    result = simulator.run(qc, shots=1).result()
    counts = result.get_counts()

    return 1 if '1' in counts else 0


def quantum_random_normal(size):
    samples = []

    for _ in range(size):
        val = 0

        # Sum of quantum bits (approx Gaussian)
        for _ in range(4):   # reduce from 8 → 4
            val += quantum_random_bit()

        # Normalize
        samples.append((val - 4) / 2)

    return samples