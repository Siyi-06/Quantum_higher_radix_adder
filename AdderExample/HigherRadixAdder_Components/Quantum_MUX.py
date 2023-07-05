#n bits MUX
import cirq

def Q_MUX(nr_qubits,cin,s0,s1):
    _qubit_order = []
    circuit = cirq.Circuit()
    qubits_cin = cirq.NamedQubit("cin")
    qubits_s0 = [cirq.NamedQubit("s0_" + str(i)) for i in range(nr_qubits)]
    qubits_s1 = [cirq.NamedQubit("s1_" + str(i)) for i in range(nr_qubits)]

    #_qubit_order
    _qubit_order.append(qubits_cin)
    initial_state = cin
    for i in range(nr_qubits):
        _qubit_order.append(qubits_s0[i])
        _qubit_order.append(qubits_s1[i])
        initial_state = initial_state+s0[i]+s1[i]
    #print("_qubit_order",_qubit_order)
    #print("initial_state", initial_state)

    #construct circuit
    for i in range(nr_qubits):
        circuit.append(cirq.CSWAP.on(qubits_cin,qubits_s0[i],qubits_s1[i]),
                            strategy = cirq.InsertStrategy.NEW)

    circuit_pic=circuit.to_text_diagram(use_unicode_characters=True,
                                          qubit_order =_qubit_order)
    print(circuit_pic)


    #simulator
    simulator = cirq.Simulator()
    initial_state = [int(initial_state[i], 2) for i in range(2* nr_qubits+1)]
    result1 = simulator.simulate(circuit,qubit_order=_qubit_order,initial_state=initial_state)
    #print(result1)
    result=str(result1)
    result=result[result.index('|')+1:-1]
    #print(result)
    real_result=""
    for i in range(nr_qubits):
        real_result=real_result+result[1+i*2]
    #print(real_result)
    summ=real_result
    #print(summ)
    return summ

if __name__ == "__main__":
    Q_MUX(nr_qubits=4,cin="1",s0="1011",s1="0001")
