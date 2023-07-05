import cirq

"""
    Implementation of Carry gate from arXiv:1611.07995v2
    Factoring using 2n+2 qubits with Toffoli based modular multiplication
"""


class CarryUsingDirtyAncilla:
    def __init__(self, nr_qubits, c):
        """
        :param c: classical constant
        :param a: quantum register
        :param g: dirty ancillae
        :param ancilla: the ancilla which will carry the result
        """
        self._qubit_order = []
        self.circuit = None

        self.c = c
        self.a = [cirq.NamedQubit("a" + str(i)) for i in range(nr_qubits)]
        self.g = [cirq.NamedQubit("g" + str(i)) for i in range(nr_qubits-1)]#n-1个脏量子位
        self.ancilla=cirq.NamedQubit("ancilla")

        self._qubit_order.append(self.a[0])
        for i in range(nr_qubits-1):
            self._qubit_order.append(self.a[i+1])
            self._qubit_order.append(self.g[i])
        self._qubit_order.append(self.ancilla)
        self.construct_circuit(nr_qubits)

    @property
    def qubit_order(self):
        return self._qubit_order

    def __str__(self):
        return self.circuit.to_text_diagram(use_unicode_characters=False,
                                          qubit_order = self.qubit_order)

    def construct_circuit(self,nr_qubits):
        self.circuit = cirq.Circuit()

        n = len(self.a)
        b = bin(self.c)[2:].zfill(n)[::-1]
        moment1 = [cirq.CNOT(self.g[-1], self.ancilla)]
        moments, moment3 = [cirq.TOFFOLI(self.a[0], self.a[1], self.g[0])], []
        if b[1] == '1':
            moments += [cirq.X(self.a[1]), cirq.CNOT(self.a[1], self.g[0])]
        for i in range(2, n):
            moments += [cirq.TOFFOLI(self.g[i - 2], self.a[i], self.g[i - 1])]
            moment3 += [cirq.TOFFOLI(self.g[i - 2], self.a[i], self.g[i - 1])]
            if b[i] == '1':
                moments += [cirq.X(self.a[i]), cirq.CNOT(self.a[i], self.g[i - 1])]
        self.circuit.append(moment1)
        self.circuit.append(moments[::-1])
        self.circuit.append(moment3)
        self.circuit.append(moment1)

        self.circuit.append(moment3[::-1])
        self.circuit.append(moments[::+1])

        return self.circuit