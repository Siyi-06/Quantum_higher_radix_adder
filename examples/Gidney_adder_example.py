import cirq
import numpy as np

from mathematics.carry_ripple_4t_adder import CarryRipple4TAdder
from utils.counting_utils import count_t_depth_of_circuit, count_t_of_circuit, count_cnot_of_circuit


def example():

    print(CarryRipple4TAdder(nr_qubits = 5, use_dual_ancilla = False))
    #print(circuit)
    ''' 
    circuit = CarryRipple4TAdder(4).construct_circuit()
    print(circuit)

    # T-depth
    print("T-depth= ", count_t_depth_of_circuit(circuit))
    # T-count
    print("T-count= ", count_t_of_circuit(circuit))
    # CNOT-count
    print("CNOT-count= ", count_cnot_of_circuit(circuit))
    # Qubit-count
    # print(qubits)
    qubits = circuit.all_qubits()
    print("qubit-count= ", len(qubits))
    simulator = cirq.Simulator()
    qubits = sorted(list(circuit.all_qubits()))[::-1]
    intial_state = [0] * 2 ** (len(qubits))
    # Setting control to '1' a to '3' and b to '1' the result should 4 = '100', a stays
    # unchaged as well as control note that ancilla1 is the most significant of the sum
    intial_state[83] = 1
    intial_state = np.array(intial_state, dtype=np.complex64)
    result = simulator.simulate(circuit, qubit_order=qubits, initial_state=intial_state)


    print(result)
    '''

def __main__():
    example()


if __name__ == "__main__":
    __main__()



