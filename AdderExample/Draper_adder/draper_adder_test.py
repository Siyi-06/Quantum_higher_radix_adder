import cirq
import utils.counting_utils as cu
import AdderExample.Draper_adder.inDraper as inDraper
import AdderExample.Draper_adder.outDraper as outDraper



def add(a, b, n, Adder,t=-1):
    A = [cirq.NamedQubit("A" + str(i)) for i in range(n)]
    B = [cirq.NamedQubit("B" + str(i)) for i in range(n)]

    circuit = cirq.Circuit()
    if rctr != 1:
        for i in range(n):
            if ((a >> i) & 1 == 1):
                circuit.append(cirq.X(A[i]))
            if ((b >> i) & 1 == 1):
                circuit.append(cirq.X(B[i]))

    if (t == -1):
        adder = Adder(A, B)
    else:
        adder = Adder(A, B, t)
    circuit.append(adder.circuit.all_operations())

    #circuit.append(cirq.measure(A, key='A'))
    #circuit.append(cirq.measure(B, key='B'))
    if rctr != 1:
        circuit.append(cirq.measure(adder.result, key="result"))

    return circuit

n=7 #bit number
a=0b111111
b=0b111111# calculate a+b

rctr = 0 # resource_count_mode
s = cirq.Simulator()
circuit=add(a,b,n, inDraper.Adder) #Here we use inplace adder as an example
results = s.simulate(circuit)
print(circuit)
output = results.measurements['result']
print(output[::-1])
print(f"T_count : {int(cu.count_t_of_circuit(circuit))}")
print(f"T_depth : {int(cu.count_t_depth_of_circuit(circuit))}")
print(f"Toffoli_depth : {int(cu.count_toffoli_depth_of_circuit(circuit))}")
print(f"Toffoli_count : {int(cu.count_toffoli_of_circuit(circuit))}")
print(f"CNOT_count : {int(cu.count_cnot_of_circuit(circuit))}")
print(f"H_count : {int(cu.count_h_of_circuit(circuit))}")
print(f"Qubit_count : {int(cirq.num_qubits(circuit))}")
print(f"Full_depth : {int(cu.count_full_depth_of_circuit(circuit))}")


