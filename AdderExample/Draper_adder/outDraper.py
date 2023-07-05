"""
  Implementation of the carry lookahead adder
  arxiv preprint 0406142
  A logarithmic-depth quantum carry-lookahead adder
"""
import cirq
import math as mt

class Adder:
    # out of place
    def __init__(self, A, B):
        """
          params: A: quantum register holding the first integer operand
          params: B: quantum register holding the second integer operand
        """
        self.A, self.B = A, B
        self.Z = [cirq.NamedQubit("Z" + str(i)) for i in range(len(self.A) + 1)]
        # n+1 크기의 결과 저장소 Z 생성
        self.circuit, self.result = self.construct_circuit()

    def w(self, n):
        return n - sum(int(mt.floor(n / (mt.pow(2, i)))) for i in range(1, int(mt.log2(n)) + 1))

    def l(self, n, t):
        return int(mt.floor(n / (mt.pow(2, t))))

    def construct_rounds(self):
        n = len(self.A)
        init = []
        p_round = []
        g_round = []
        c_round = []

        length = n - self.w(n) - mt.floor(mt.log2(n))
        ancilla = [cirq.NamedQubit("a" + str(i)) for i in range(length)]  # 논문에서 X라 지칭

        # Init round
        for i in range(n):
            init.append(cirq.TOFFOLI(self.A[i], self.B[i], self.Z[i + 1]))

        for i in range(1,n):
            init.append(cirq.CNOT(self.A[i], self.B[i]))

        # P-round
        idx = 0  # ancilla idx
        tmp = 0 # m=1일 때 idx 저장해두기
        for t in range(1, int(mt.log2(n))):
            pre = tmp  # (t-1)일 때의 첫번째 자리 저장
            for m in range(1, self.l(n, t)):
                if t == 1: # B에 저장되어있는 애들로만 연산 가능
                    p_round.append(cirq.TOFFOLI(self.B[2*m], self.B[2*m+1], ancilla[idx]))
                else: # t가 1보다 클 때는 ancilla에 저장된 애들도 이용해야함
                    p_round.append(cirq.TOFFOLI(ancilla[pre-1+2*m], ancilla[pre-1+2*m+1], ancilla[idx]))
                    # p_round.append(cirq.TOFFOLI(ancilla[idx-self.l(n,t-1)+2*m], ancilla[idx-self.l(n,t-1)+2*m+1], ancilla[idx]))
                    # 이건 절대적 위치 계산한 식임. 이것도 제대로 동작하긴 함.
                if m==1:
                    tmp = idx
                idx += 1


        # G-round
        pre = -1 # 맨처음엔 이전자리가 없으니까
        idx = -1 # ancilla idx
        for t in range(1, int(mt.log2(n))+1):
            for m in range(self.l(n, t)):
                if t == 1: # B에 저장되어있는 애들로만 연산 가능
                    g_round.append(cirq.TOFFOLI(self.Z[int(mt.pow(2, t)*m + mt.pow(2, t-1))], self.B[2 * m + 1], self.Z[int(mt.pow(2, t)*(m+1))]))
                else: # t가 1보다 클 때는 ancilla에 저장된 애들도 이용해야함
                    idx = pre+2*m+1
                    g_round.append(cirq.TOFFOLI(self.Z[int(mt.pow(2, t)*m + mt.pow(2, t-1))], ancilla[idx], self.Z[int(mt.pow(2, t)*(m+1))]))
            pre = idx # t-1의 맨마지막

        # C-round
        # 이거 순서대로 담고 마지막에 뒤집어도 될 듯
        for t in range(int(mt.log2(2*n/3)),0,-1):
            idx = len(ancilla) - 1 - (self.l((n - pow(2, t - 1)), t) + self.l((n - pow(2, t - 2)),t - 1))  # 현재 접근하고자하는 P의 시작 index -1.
            for m in range(1,self.l((n-pow(2,t-1)), t)+1):
                if t == 1:  # B에 저장되어있는 애들로만 연산 가능
                    c_round.append(
                        cirq.TOFFOLI(self.Z[int(mt.pow(2, t) * m)], self.B[2 * m], self.Z[int(mt.pow(2, t) * m + mt.pow(2, t - 1))]))
                else:
                    c_round.append(cirq.TOFFOLI(self.Z[int(mt.pow(2, t) * m)], ancilla[idx+2*m],self.Z[int(mt.pow(2, t) * m + mt.pow(2, t - 1))]))


        # Last round
        last_round = [cirq.CNOT(self.B[i], self.Z[i]) for i in range(n)]
        last_round += [cirq.CNOT(self.A[0], self.Z[0])]
        last_round += [cirq.CNOT(self.A[i], self.B[i]) for i in range(1, n)]

        return init, p_round, g_round, c_round, last_round

    def construct_circuit(self):
        """
          returns the CLA circuit
        """

        """
          Computation part of the circuit
        """
        init_comp, p_round_comp, g_round_comp, c_round_comp, last_round = self.construct_rounds()

        circuit = cirq.Circuit()

        # Init
        circuit += init_comp

        # P-round
        circuit += p_round_comp

        # G-round
        circuit += g_round_comp

        # C-round
        circuit += c_round_comp

        # P-inverse
        circuit += p_round_comp[::-1]

        # Last round
        circuit += last_round

        result = []

        for k in self.Z:
            result.append(k)

        # print(circuit)
        return circuit, result
