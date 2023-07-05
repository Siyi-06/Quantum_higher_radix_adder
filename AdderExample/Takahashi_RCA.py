#https://arxiv.org/abs/0910.2530
#Quantum Addition Circuits and Unbounded Fan-Out
#输入n,构建n位Takahashi Adder
#输出电路图 + 4个指标


#！！！！！还有两个别的adder

import cirq
import mathematics
from mathematics.takahashi0910 import TakahashiAdder
from utils.counting_utils import *
from qramcircuits.toffoli_decomposition import *

def main():

    #决定n位加法器
    nr_qubits = input("请输入一个整数：")
    # python中input函数输出的是一个字符串，而只有通过int进行强制转换
    nr_qubits = int(nr_qubits)

    # 构造电路
    A=[cirq.NamedQubit("a" + str(i)) for i in range(nr_qubits)]
    B=[cirq.NamedQubit("b" + str(i)) for i in range(nr_qubits)]

    c=TakahashiAdder(nr_qubits,A, B, ancillae=None, type = True).construct_circuit()
    print(c)
    #Toffoli分解
    ct=cirq.Circuit(ToffoliDecomposition.construct_decomposed_moments(c.moments, ToffoliDecompType.ZERO_ANCILLA_TDEPTH_2_COMPUTE))

   #分解后电路
    print(ct)
    
    
    # T-count、T-depth、Qubit-count、CNOT-count
    print("分解前电路")
    print("T-depth= ", count_t_depth_of_circuit(c))
    print("T-count= ", count_t_of_circuit(c))
    # print("CNOT-count= ", count_cnot_of_circuit(c))
    print("Qubit-count=", len(c.all_qubits()))
    print("Toffoli-count=", count_toffoli_of_circuit(c))#2n-1

    print("分解后电路")
    print("Qubit-count=", len(ct.all_qubits()))  # 2n+1
    print("T-depth= ", count_t_depth_of_circuit(ct))  # 4n-2
    print("T-count= ", count_t_of_circuit(ct))  # 8n-4


if __name__ == "__main__":
    main()
