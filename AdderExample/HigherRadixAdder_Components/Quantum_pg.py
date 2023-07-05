#n bits propagate and generate
import cirq
def Q_pg(nr_qubits,a,b):
    _qubit_order = []
    circuit = cirq.Circuit()
    initial_state=""
    qubits_a = [cirq.NamedQubit("a" + str(i)) for i in range(nr_qubits)]
    qubits_b = [cirq.NamedQubit("b" + str(i)) for i in range(nr_qubits)]
    qubits_g = [cirq.NamedQubit("g" + str(i)) for i in range(nr_qubits)]

    #_qubit_order
    for i in range(nr_qubits):
        _qubit_order.append(qubits_a[i])
        _qubit_order.append(qubits_b[i])
        _qubit_order.append(qubits_g[i])
        initial_state = initial_state+a[i]+b[i]+str(0)
    #print(_qubit_order,initial_state)

    #construct circuit
    for i in range(nr_qubits):
        circuit.append(cirq.CCNOT.on(qubits_a[i],qubits_b[i],qubits_g[i]),
                            strategy = cirq.InsertStrategy.NEW)
        circuit.append(cirq.CNOT.on(qubits_a[i],qubits_b[i]),
                       strategy=cirq.InsertStrategy.NEW)

    circuit_pic=circuit.to_text_diagram(use_unicode_characters=True,
                                          qubit_order =_qubit_order)
    print(circuit_pic)



    #simulator
    simulator = cirq.Simulator()
    initial_state = [int(initial_state[i], 2) for i in range(3* nr_qubits)]
    result1 = simulator.simulate(circuit,qubit_order=_qubit_order,initial_state=initial_state)
    #print(result1)
    result=str(result1)
    result=result[result.index('|')+1:-1]
    #print(result)
    p=""
    g=""
    for i in range(nr_qubits):
        p = p + result[1 + i * 3]
        g = g + result[2 + i * 3]
    return p,g


def Q_pg_decomputation(nr_qubits,a,b,radix_num):
    _qubit_order = []
    circuit = cirq.Circuit()
    initial_state=""
    qubits_a = [cirq.NamedQubit("a" + str(i)) for i in range(nr_qubits)]
    qubits_b = [cirq.NamedQubit("b" + str(i)) for i in range(nr_qubits)]
    qubits_g = [cirq.NamedQubit("g" + str(i)) for i in range(nr_qubits)]

    #_qubit_order
    for i in range(nr_qubits):
        _qubit_order.append(qubits_a[i])
        _qubit_order.append(qubits_b[i])
        _qubit_order.append(qubits_g[i])
        initial_state = initial_state+a[i]+b[i]+str(0)
    #print(_qubit_order,initial_state)

    #construct circuit
    for i in range(nr_qubits):
        circuit.append(cirq.CNOT.on(qubits_a[i],qubits_b[i]),
                       strategy=cirq.InsertStrategy.NEW)
        if i%radix_num==0:
            circuit.append(cirq.CCNOT.on(qubits_a[i],qubits_b[i],qubits_g[i]),
                            strategy = cirq.InsertStrategy.NEW)
    circuit_pic=circuit.to_text_diagram(use_unicode_characters=True,
                                          qubit_order =_qubit_order)
    print(circuit_pic)



    #simulator
    simulator = cirq.Simulator()
    initial_state = [int(initial_state[i], 2) for i in range(3* nr_qubits)]
    result1 = simulator.simulate(circuit,qubit_order=_qubit_order,initial_state=initial_state)
    #print(result1)
    result=str(result1)
    result=result[result.index('|')+1:-1]
    #print(result)
    p=""
    g=""
    for i in range(nr_qubits):
        p = p + result[1 + i * 3]
        g = g + result[2 + i * 3]
    return p,g

if __name__ == "__main__":
    #Q_pg(nr_qubits=4,a="1011",b="0001")
    Q_pg_decomputation(nr_qubits=4, a="1011", b="0001",radix_num=3)
