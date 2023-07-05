#输入n,构建n位VBE Adder（新的）
#输出电路图 + 4个指标
import cirq
import mathematics
from mathematics import VBEAdder
from utils.counting_utils import *
from qramcircuits.toffoli_decomposition import *

def main():
    #思路相同，构建电路+分解（但是论文没有说明分解方法！！！）
    #决定n位加法器
    nr_qubits = input("请输入一个整数：")
    # python中input函数输出的是一个字符串，而只有通过int进行强制转换
    nr_qubits = int(nr_qubits)

    #构造电路！！！！！！
    c=VBEAdder(nr_qubits).construct_circuit(nr_qubits)#cirq circuit
    c1=VBEAdder(nr_qubits)#VBE adder object

    #电路情况
    print(c1)#电路图

    # Decomposition: 暂定使用A0T2
    ct = cirq.Circuit(
        ToffoliDecomposition.construct_decomposed_moments(c.moments, ToffoliDecompType.ZERO_ANCILLA_TDEPTH_2_COMPUTE))
    print(ct)
    # T-count、T-depth、Qubit-count、CNOT-count
    print("分解前电路")
    print("T-depth= ", count_t_depth_of_circuit(c))
    print("T-count= ", count_t_of_circuit(c))
    print("CNOT-count= ", count_cnot_of_circuit(c))
    print("Qubit-count=", len(c.all_qubits()))
    print("Toffoli-count=", count_toffoli_of_circuit(c))

    print("分解后电路")
    print("Qubit-count=", len(ct.all_qubits()))  # 2n+2
    print("T-depth= ", count_t_depth_of_circuit(ct))  # 4n
    print("T-count= ", count_t_of_circuit(ct))  # 8n

    #simulator
    '''
    VBE_qubit_order = VBEAdder(nr_qubits).qubit_order
    print(VBE_qubit_order)
    simulator = cirq.Simulator()
    result = simulator.simulate(c,qubit_order=VBE_qubit_order,initial_state=0b0110000110)
    print("Results:")
    print(result)
    '''


if __name__ == "__main__":
    main()
