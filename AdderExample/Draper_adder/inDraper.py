"""
  Implementation of the carry lookahead adder
  arxiv preprint 0406142
  A logarithmic-depth quantum carry-lookahead adder
"""
import cirq
import math as mt

class Adder:
    # in-place
    def __init__(self, A, B):
        """
          params: A: quantum register holding the first integer operand
          params: B: quantum register holding the second integer operand
        """
        self.A, self.B = A, B
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
        p_round_uncomp = []
        g_round_uncomp = []
        c_round_uncomp = []

        length = n - self.w(n) - mt.floor(mt.log2(n))
        ancilla1 = [cirq.NamedQubit("z" + str(i)) for i in range(n)]  # z[1] ~ z[n] 저장
        ancilla2 = [cirq.NamedQubit("a" + str(i)) for i in range(length)] # 논문에서 X라고 지칭되는 ancilla

        # Init round
        for i in range(n):
            init.append(cirq.TOFFOLI(self.A[i], self.B[i], ancilla1[i])) # ancilla1[0] == Z[1]
        for i in range(n):
            init.append(cirq.CNOT(self.A[i], self.B[i]))

        # P-round
        idx = 0  # ancilla idx
        tmp = 0 # m=1일 때 idx 저장해두기
        pivot = 0 # (n-1) adder일 때 배열 끊는 기준
        for t in range(1, int(mt.log2(n))):
            pre = tmp  # (t-1)일 때의 첫번째 자리 저장
            for m in range(1, self.l(n, t)):
                if t == 1: # B에 저장되어있는 애들로만 연산 가능
                    p_round.append(cirq.TOFFOLI(self.B[2*m], self.B[2*m+1], ancilla2[idx]))
                else: # t가 1보다 클 때는 ancilla에 저장된 애들도 이용해야함
                    p_round.append(cirq.TOFFOLI(ancilla2[pre-1+2*m], ancilla2[pre-1+2*m+1], ancilla2[idx]))
                    # p_round.append(cirq.TOFFOLI(ancilla[idx-self.l(n,t-1)+2*m], ancilla[idx-self.l(n,t-1)+2*m+1], ancilla[idx]))
                    # 이건 절대적 위치 계산한 식임. 이것도 제대로 동작하긴 함.
                if m == 1:
                    tmp = idx
                idx += 1

            # uncomp part
            if self.l(n, t) == self.l(n - 1, t):
                p_round_uncomp += p_round[pivot:]
                pivot = len(p_round)
            else:
                p_round_uncomp += p_round[pivot:-1]
                pivot = len(p_round)

        if n!=1 and int(mt.log2(n)) != int(mt.log2(n-1)):
            p_round_uncomp = p_round_uncomp[:-(self.l(n, int(mt.log2(n))-1)-1)] # 잘못 추가된거 삭제

        # G-round
        pre = -1  # 맨처음엔 이전자리가 없으니까
        idx = -1  # ancilla idx
        pivot = 0
        for t in range(1, int(mt.log2(n))+1):
            for m in range(self.l(n, t)):
                if t == 1: # B에 저장되어있는 애들로만 연산 가능
                    g_round.append(cirq.TOFFOLI(ancilla1[int(mt.pow(2, t)*m + mt.pow(2, t-1))-1], self.B[2 * m + 1], ancilla1[int(mt.pow(2, t)*(m+1))-1]))
                else: # t가 1보다 클 때는 ancilla에 저장된 애들도 이용해야함
                    idx = pre+2*m+1
                    g_round.append(cirq.TOFFOLI(ancilla1[int(mt.pow(2, t)*m + mt.pow(2, t-1))-1], ancilla2[idx], ancilla1[int(mt.pow(2, t)*(m+1))-1]))
            pre = idx # t-1의 맨마지막

            # uncomp part
            if self.l(n, t) == self.l(n - 1, t):
                g_round_uncomp += g_round[pivot:]
                pivot = len(g_round)
            else:
                g_round_uncomp += g_round[pivot:-1]
                pivot = len(g_round)

        if n!=1 and int(mt.log2(n)) != int(mt.log2(n - 1)):
            g_round_uncomp = g_round_uncomp[:-(self.l(n, int(mt.log2(n))) - 1)]  # 잘못 추가된거 삭제

        # C-round
        # 이거 순서대로 담고 마지막에 뒤집어도 될 듯
        pivot = 0
        for t in range(int(mt.log2(2*n/3)),0,-1):
            idx = len(ancilla2) - 1 - (self.l((n - pow(2, t - 1)), t) + self.l((n - pow(2, t - 2)),t - 1))  # 현재 접근하고자하는 P의 시작 index -1.
            for m in range(1,self.l((n-pow(2,t-1)), t)+1):
                if t == 1:  # B에 저장되어있는 애들로만 연산 가능
                    c_round.append(
                        cirq.TOFFOLI(ancilla1[int(mt.pow(2, t) * m)-1], self.B[2 * m], ancilla1[int(mt.pow(2, t) * m + mt.pow(2, t - 1))-1]))
                else:
                    c_round.append(cirq.TOFFOLI(ancilla1[int(mt.pow(2, t) * m)-1], ancilla2[idx+2*m],ancilla1[int(mt.pow(2, t) * m + mt.pow(2, t - 1))-1]))

            # uncomp part
            if self.l((n-pow(2,t-1)), t) == self.l(((n-1)-pow(2,t-1)), t):
                c_round_uncomp += c_round[pivot:]
                pivot = len(c_round)
            else:
                c_round_uncomp += c_round[pivot:-1]
                pivot = len(c_round)

        t = int(mt.log2(2*n/3))
        if n!=1 and int(mt.log2(2*n/3)) != int(mt.log2(2*(n-1)/3)):
            c_round_uncomp = c_round_uncomp[:self.l((n-pow(2,t-1)), t)-1]+c_round_uncomp[self.l((n-pow(2,t-1)), t):] # 잘못 추가된거 삭제

        # Last round
        last_round = [cirq.CNOT(ancilla1[i-1], self.B[i]) for i in range(1, n)]
        last_round += [cirq.X(self.B[i]) for i in range(n-1)]
        last_round += [cirq.CNOT(self.A[i], self.B[i]) for i in range(1, n-1)]

        return init, p_round, g_round, c_round, last_round, p_round_uncomp, g_round_uncomp, c_round_uncomp, ancilla1

    def construct_circuit(self):
        """
          returns the CLA circuit
        """

        """
          Computation part of the circuit
        """
        init_comp, p_round_comp, g_round_comp, c_round_comp, last_round, p_round_uncomp, g_round_uncomp, c_round_uncomp, ancilla = self.construct_rounds()
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

        ### Step7. Section3 in reverse. (n-1)bit adder ###
        n = len(self.A)

        circuit += p_round_uncomp
        circuit += c_round_uncomp[::-1]
        circuit += g_round_uncomp[::-1]
        circuit += p_round_uncomp[::-1]

        '''
        ### Step7. Section3 in reverse. (n-1)bit adder ###

        p_round_uncomp = 0
        # P round에서 어디까지 잘라야하는지 계산. 방식을 개선시킬 수 있을 것 같지만 일단 보류.
        start = 0
        end = 0
        for t in range(1, int(mt.log2(n - 1))):
            for m in range(1, int(mt.floor((n - 1) / (mt.pow(2, t))))):
                end += 1
            p_round_uncomp += p_round_comp[start:end+1] # 기존 P-round 자르기
            start = int(mt.floor((n) / (mt.pow(2, t))))-1

        #print(cnt)

        p_round_uncomp = p_round_comp[:cnt] # 기존 P-round 자르기
        circuit += cirq.Circuit(p_round_uncomp)

        # C
        cnt = 0
        for t in range(int(mt.log2(2*(n-1)/3)),0,-1):
            for m in range(1,self.l(((n-1)-pow(2,t-1)), t)+1):
                cnt += 1


        c_round_uncomp = c_round_comp[:cnt][::-1] # 기존 C-round 자르기 -> 뒤집기
        circuit += cirq.Circuit(c_round_uncomp)

        # G
        cnt = 0
        for t in range(1, int(mt.log2(n-1)) + 1):
            for m in range(self.l(n-1, t)):
                cnt += 1

        g_round_uncomp = g_round_comp[:cnt][::-1]
        circuit += cirq.Circuit(g_round_uncomp)

        # P^(-1)
        circuit += cirq.Circuit(p_round_uncomp[::-1])
        
        '''

        fin = [cirq.CNOT(self.A[i], self.B[i]) for i in range(1,n-1)]
        fin += [cirq.TOFFOLI(self.A[i], self.B[i], ancilla[i]) for i in range(n - 1)]
        fin += [cirq.X(self.B[i]) for i in range(n - 1)]

        circuit.append(fin)

        result = []

        for k in self.B:
            result.append(k)
        result.append(ancilla[-1])

        # print(circuit)
        return circuit, result
