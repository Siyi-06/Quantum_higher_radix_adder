#High radix layer, radix_num = radix
import cirq
import numpy as np
import math

def CnNOT(n):
    return cirq.ControlledGate(cirq.CCNOT, n-2)


def High_radix_layer(nr_qubits,radix,p,g):
    _qubit_order = []
    initial_state =""
    j=0
    circuit = cirq.Circuit()
    qubits_p = [cirq.NamedQubit("p" + str(i)) for i in range(nr_qubits)]
    qubits_g = [cirq.NamedQubit("g" + str(i)) for i in range(nr_qubits)]
    qubits_p_new = [cirq.NamedQubit("p_new" + str(i)) for i in range(nr_qubits)]

    #_qubit_order
    for i in range(nr_qubits):
        _qubit_order.append(qubits_p[i])
        _qubit_order.append(qubits_g[i])
        initial_state = initial_state + p[i] + g[i]
        if ((i+1)%radix) ==0:
            _qubit_order.append(qubits_p_new[j])
            j = j + 1
            initial_state = initial_state+str(0)
    #print(_qubit_order,initial_state)

    #propagate
    C_r_NOT=CnNOT(radix)
    for i in range(math.floor(nr_qubits/radix)):
        #print(qubits_p[i*radix:(i+1)*radix],qubits_p_new[i:i+1])
        circuit.append(C_r_NOT(*qubits_p[i*radix:(i+1)*radix], *qubits_p_new[i:i+1]))


    # generate

    for i in range(math.floor(nr_qubits/radix)):
        for k in range(radix-1):
            #print(qubits_g[i*radix+k:i*radix+k+1],qubits_p[i*radix+k+1:i*radix+k+2],qubits_g[i*radix+k+1:i*radix+k+2])
            circuit.append(cirq.CCNOT(*qubits_g[i*radix+k:i*radix+k+1], *qubits_p[i*radix+k+1:i*radix+k+2],*qubits_g[i*radix+k+1:i*radix+k+2]))



    circuit_pic = circuit.to_text_diagram(use_unicode_characters=True,
                                          qubit_order=_qubit_order)
    print(circuit_pic)



    #simulator
    simulator = cirq.Simulator()
    initial_state = [int(initial_state[i], 2) for i in range(len(initial_state))]
    result1 = simulator.simulate(circuit,qubit_order=_qubit_order,initial_state=initial_state)
    #print(result1)
    result=str(result1)
    result=result[result.index('|')+1:-1]
    #print(result)
    p_pairs=""
    g_pairs=""
    for i in range(1,math.floor(nr_qubits/radix)+1):
        #7,6    14,13; 6 5    13 12
        p_pairs = p_pairs + result[(2*radix+1)*i-1]
        g_pairs = g_pairs + result[(2*radix+1)*i-2]
        #print((2*radix+1)*i-1,(2*radix+1)*i-1-1)
    #print(p_pairs, g_pairs)
    return p_pairs,g_pairs


if __name__ == "__main__":
    p="111001"
    g="000000"
    High_radix_layer(nr_qubits=6,radix=3, p=p,g=g)