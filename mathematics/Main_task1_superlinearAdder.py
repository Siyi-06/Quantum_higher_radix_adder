
import cirq

from utils.counting_utils import count_t_depth_of_circuit, count_cnot_of_circuit, count_t_of_circuit
from .recycled_gate import RecycledGate

class SuperlinearAdder():
    def __init__(self, nr_qubits = 3):
        #print("VBE Adder")
        self._qubit_order = []
        self.circuit = None
        #!!!!!!!
    @property
    def qubit_order(self):
        return self._qubit_order

    def __str__(self):
        return self.circuit.to_text_diagram(use_unicode_characters=False,
                                          qubit_order = self.qubit_order)

    def construct_circuit(self, nr_qubits):


        return self.circuit