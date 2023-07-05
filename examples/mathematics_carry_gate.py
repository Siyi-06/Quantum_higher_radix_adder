import cirq

from mathematics import CarryUsingDirtyAncilla
from utils.counting_utils import count_t_depth_of_circuit, count_t_of_circuit, count_cnot_of_circuit

a = [cirq.NamedQubit("a" + str(i)) for i in range(4)]
g = [cirq.NamedQubit("g" + str(i)) for i in range(3)]
r = cirq.NamedQubit("r")

carry = CarryUsingDirtyAncilla(a, 11, g, r).construct_circuit()

#Circuit diagram
print(carry)
#T-depth
print(count_t_depth_of_circuit(carry))
#T-count
print(count_t_of_circuit(carry))
#CNOT-count
print(count_cnot_of_circuit(carry))
#Qubit-count
#print(qubits)
qubits = carry.all_qubits()
print(len(qubits))