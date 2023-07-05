'''
《Quantum Carry-Save Arithmetic》
https://arxiv.org/abs/quant-ph/9808061
'''
import cirq
import mathematics
from mathematics import CarryUsingDirtyAncilla
from utils.counting_utils import *
from qramcircuits.toffoli_decomposition import *

#structure 1: QFA
def Quantum_full_adder_sample(a,b,c,d):
    print("structure 1: QFA")
    _qubit_order = []
    circuit = cirq.Circuit()
    initial_state=""
    qubits_a = cirq.NamedQubit("a")
    qubits_b = cirq.NamedQubit("b")
    qubits_c = cirq.NamedQubit("c")
    qubits_d = cirq.NamedQubit("d")

    #_qubit_order
    _qubit_order.append(qubits_a)
    _qubit_order.append(qubits_b)
    _qubit_order.append(qubits_c)
    _qubit_order.append(qubits_d)
    initial_state = initial_state+str(a)+str(b)+str(c)+str(d)
    #print(_qubit_order,initial_state)

    #construct circuit
    circuit.append(cirq.CCNOT.on(qubits_b,qubits_c,qubits_d),
                            strategy = cirq.InsertStrategy.NEW)
    circuit.append(cirq.CNOT.on(qubits_b,qubits_c),
                       strategy=cirq.InsertStrategy.NEW)
    circuit.append(cirq.CCNOT.on(qubits_a,qubits_c,qubits_d),
                            strategy = cirq.InsertStrategy.NEW)
    circuit.append(cirq.CNOT.on(qubits_a,qubits_c),
                       strategy=cirq.InsertStrategy.NEW)
    circuit_pic=circuit.to_text_diagram(use_unicode_characters=True,
                                          qubit_order =_qubit_order)
    print(circuit_pic)



    #simulator
    simulator = cirq.Simulator()
    initial_state = [int(initial_state[i], 2) for i in range(4)]
    print("initial_state",initial_state)
    result1 = simulator.simulate(circuit,qubit_order=_qubit_order,initial_state=initial_state)
    #print("result1",result1)
    result=str(result1)
    result=result[result.index('|')+1:-1]
    print("result",result)

#structure 2: QMG
def Quantum_majority_gate_sample(a,b,c,d):
    print("structure 2: QMG")
    _qubit_order = []
    circuit = cirq.Circuit()
    initial_state=""
    qubits_a = cirq.NamedQubit("a")
    qubits_b = cirq.NamedQubit("b")
    qubits_c = cirq.NamedQubit("c")
    qubits_d = cirq.NamedQubit("d")

    #_qubit_order
    _qubit_order.append(qubits_a)
    _qubit_order.append(qubits_b)
    _qubit_order.append(qubits_c)
    _qubit_order.append(qubits_d)
    initial_state = initial_state+str(a)+str(b)+str(c)+str(d)
    #print(_qubit_order,initial_state)

    #construct circuit
    circuit.append(cirq.CCNOT.on(qubits_b,qubits_c,qubits_d),
                            strategy = cirq.InsertStrategy.NEW)
    circuit.append(cirq.CNOT.on(qubits_b,qubits_c),
                       strategy=cirq.InsertStrategy.NEW)
    circuit.append(cirq.CCNOT.on(qubits_a,qubits_c,qubits_d),
                            strategy = cirq.InsertStrategy.NEW)
    circuit.append(cirq.CNOT.on(qubits_b,qubits_c),
                       strategy=cirq.InsertStrategy.NEW)
    circuit_pic=circuit.to_text_diagram(use_unicode_characters=True,
                                          qubit_order =_qubit_order)
    print(circuit_pic)

    #simulator
    simulator = cirq.Simulator()
    initial_state = [int(initial_state[i], 2) for i in range(4)]
    print("initial_state",initial_state)
    result1 = simulator.simulate(circuit,qubit_order=_qubit_order,initial_state=initial_state)
    #print("result1",result1)
    result=str(result1)
    result=result[result.index('|')+1:-1]
    print("result",result)
    return 0

#component 1: QFA
def QFA(circuit,qubits_a,qubits_b,qubits_c,qubits_d):
    circuit.append(cirq.CCNOT.on(qubits_b,qubits_c,qubits_d),
                            strategy = cirq.InsertStrategy.NEW)
    circuit.append(cirq.CNOT.on(qubits_b,qubits_c),
                       strategy=cirq.InsertStrategy.NEW)
    circuit.append(cirq.CCNOT.on(qubits_a,qubits_c,qubits_d),
                            strategy = cirq.InsertStrategy.NEW)
    circuit.append(cirq.CNOT.on(qubits_a,qubits_c),
                       strategy=cirq.InsertStrategy.NEW)
def De_QFA(circuit,qubits_a,qubits_b,qubits_c,qubits_d):
    circuit.append(cirq.CNOT.on(qubits_a,qubits_c),
                       strategy=cirq.InsertStrategy.NEW)
    circuit.append(cirq.CCNOT.on(qubits_a,qubits_c,qubits_d),
                            strategy = cirq.InsertStrategy.NEW)
    circuit.append(cirq.CNOT.on(qubits_b,qubits_c),
                       strategy=cirq.InsertStrategy.NEW)
    circuit.append(cirq.CCNOT.on(qubits_b,qubits_c,qubits_d),
                            strategy = cirq.InsertStrategy.NEW)



#component 2: QMG
def QMG(circuit,qubits_a,qubits_b,qubits_c,qubits_d):
    circuit.append(cirq.CCNOT.on(qubits_b,qubits_c,qubits_d),
                            strategy = cirq.InsertStrategy.NEW)
    circuit.append(cirq.CNOT.on(qubits_b,qubits_c),
                       strategy=cirq.InsertStrategy.NEW)
    circuit.append(cirq.CCNOT.on(qubits_a,qubits_c,qubits_d),
                            strategy = cirq.InsertStrategy.NEW)
    circuit.append(cirq.CNOT.on(qubits_b,qubits_c),
                       strategy=cirq.InsertStrategy.NEW)

#structure 3: Quantum Ripple-Carry Adder
def Quantum_Ripple_Carry_Adder(nr_qubits,a,b):
    _qubit_order = []
    circuit = cirq.Circuit()
    initial_state=""
    qubits_a = [cirq.NamedQubit("a" + str(i)) for i in range(nr_qubits)]
    qubits_b = [cirq.NamedQubit("b" + str(i)) for i in range(nr_qubits)]
    qubits_ancilla = [cirq.NamedQubit("ancilla" + str(i)) for i in range(nr_qubits+1)]

    #_qubit_order
    initial_state = initial_state+str(0)
    _qubit_order.append(qubits_ancilla[0])
    for i in range(nr_qubits):
        _qubit_order.append(qubits_a[i])
        _qubit_order.append(qubits_b[i])
        _qubit_order.append(qubits_ancilla[i+1])
        initial_state = initial_state+a[i]+b[i]+str(0)
    print(_qubit_order,initial_state)

    #construct circuit
    for i in range(nr_qubits):
        QFA(circuit,qubits_ancilla[i],qubits_a[i],qubits_b[i],qubits_ancilla[i+1])
    for i in range(nr_qubits-2,-1,-1):
        print("i",i)
        QMG(circuit,qubits_ancilla[i],qubits_a[i],qubits_b[i],qubits_ancilla[i+1])


    circuit_pic=circuit.to_text_diagram(use_unicode_characters=True,
                                          qubit_order =_qubit_order)
    print(circuit_pic)

    #simulator
    simulator = cirq.Simulator()
    initial_state = [int(initial_state[i], 2) for i in range(3*nr_qubits+1)]
    print("initial_state",initial_state)
    result1 = simulator.simulate(circuit,qubit_order=_qubit_order,initial_state=initial_state)
    #print("result1",result1)
    result=str(result1)
    result=result[result.index('|')+1:-1]
    print("result",result)

    num_a=""
    summ=""
    for i in range(nr_qubits):
        num_a = num_a + result[1 + i * 3]
        summ = summ + result[2 + i * 3]
    print("num_a",num_a)
    print("summ",summ)

#structure 4: Quantum Carry-Save Adder
#Branch 1: 3->2
#http://t.csdn.cn/VNrcR
def Quantum_Carry_Save_Adder_3_2(a,b,c):
    print("structure 4: Quantum Carry-Save Adder")
    print("Branch 1: 3->2 = Quantum_full_adder")
    _qubit_order = []
    circuit = cirq.Circuit()
    initial_state=""
    qubits_a = cirq.NamedQubit("a")
    qubits_b = cirq.NamedQubit("b")
    qubits_c = cirq.NamedQubit("c")
    qubits_0 = cirq.NamedQubit("0")

    #_qubit_order
    _qubit_order.append(qubits_a)
    _qubit_order.append(qubits_b)
    _qubit_order.append(qubits_c)
    _qubit_order.append(qubits_0)
    initial_state = initial_state+str(a)+str(b)+str(c)+str(0)
    #print(_qubit_order,initial_state)

    #construct circuit
    QFA(circuit,qubits_a,qubits_b,qubits_c,qubits_0)
    circuit_pic=circuit.to_text_diagram(use_unicode_characters=True,
                                          qubit_order =_qubit_order)
    #print(circuit_pic)

    #simulator
    simulator = cirq.Simulator()
    initial_state = [int(initial_state[i], 2) for i in range(3+1+(3-3))]
    print("initial_state",initial_state)
    result1 = simulator.simulate(circuit,qubit_order=_qubit_order,initial_state=initial_state)
    #print("result1",result1)
    result=str(result1)
    result=result[result.index('|')+1:-1]
    print("result",result)

    print("s", result[-2])
    print("k",result[-1])


#Branch 2: 4->2
def Quantum_Carry_Save_Adder_4_2(a,b,c,d):
    print("structure 4: Quantum Carry-Save Adder")
    print("Branch 2: 4->2")
    _qubit_order = []
    circuit = cirq.Circuit()
    initial_state=""
    qubits_a = cirq.NamedQubit("a")
    qubits_b = cirq.NamedQubit("b")
    qubits_c = cirq.NamedQubit("c")
    qubits_d = cirq.NamedQubit("d")
    qubits_ancilla = [cirq.NamedQubit("ancilla" + str(i)) for i in range(3)]

    #_qubit_order
    _qubit_order.append(qubits_a)
    _qubit_order.append(qubits_b)
    _qubit_order.append(qubits_c)
    _qubit_order.append(qubits_ancilla[0])
    _qubit_order.append(qubits_d)
    _qubit_order.append(qubits_ancilla[1])
    _qubit_order.append(qubits_ancilla[2])
    initial_state = initial_state+str(a)+str(b)+str(c)+str(0)+str(d)+str(0)+str(0)
    #print(_qubit_order,initial_state)

    #construct circuit
    QFA(circuit,qubits_a,qubits_b,qubits_c,qubits_ancilla[0])
    QFA(circuit, qubits_c, qubits_ancilla[2],qubits_d,qubits_ancilla[1])
    De_QFA(circuit, qubits_a, qubits_b, qubits_c, qubits_ancilla[0])
    circuit_pic=circuit.to_text_diagram(use_unicode_characters=True,
                                          qubit_order =_qubit_order)
    print(circuit_pic)

    #simulator
    simulator = cirq.Simulator()
    initial_state = [int(initial_state[i], 2) for i in range(4+2+(4-3))]
    print("initial_state",initial_state)
    result1 = simulator.simulate(circuit,qubit_order=_qubit_order,initial_state=initial_state)
    #print("result1",result1)
    result=str(result1)
    result=result[result.index('|')+1:-1]
    print("result",result)

    print("k_next",result[-2])
    print("s",result[-3])
#def Quantum_Carry_Save_Adder_8_2(a, b, c, d):

def main():
    '''
    Quantum_full_adder_sample(a=1,b=0,c=0,d=0)
    print("")
    Quantum_majority_gate_sample(a=1,b=0,c=0,d=0)
    print("")

    #from low->high
    Quantum_Ripple_Carry_Adder(nr_qubits=4,a="1011",b="0101")
    print("")

    Quantum_full_adder_sample(a=1,b=0,c=0,d=0)
    print("")
    '''


    '''
    #要组合起来，Carry Save Adder属于一个component！！！
    Quantum_Carry_Save_Adder_3_2(a=1,b=0,c=0)
    print("")
    Quantum_Carry_Save_Adder_3_2(a=1,b=0,c=0)
    print("")
    Quantum_Carry_Save_Adder_3_2(a=1,b=0,c=0)
    print("")
    Quantum_Carry_Save_Adder_3_2(a=1,b=1,c=0)
    print("")
    '''

    Quantum_Carry_Save_Adder_4_2(a=0, b=0, c=0, d=0)
    Quantum_Carry_Save_Adder_4_2(a=0, b=0, c=0, d=1)
    Quantum_Carry_Save_Adder_4_2(a=0, b=0, c=1, d=0)
    Quantum_Carry_Save_Adder_4_2(a=1, b=0, c=0, d=1)
    print("1100!!!")
    Quantum_Carry_Save_Adder_4_2(a=1, b=0, c=1, d=0)
    Quantum_Carry_Save_Adder_4_2(a=1, b=1, c=1, d=0)
    Quantum_Carry_Save_Adder_4_2(a=1, b=1, c=0, d=1)
    Quantum_Carry_Save_Adder_4_2(a=1, b=1, c=1, d=1)
    print("")


if __name__ == "__main__":
    main()