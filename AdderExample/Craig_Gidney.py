#输入n,构建n位Craig-Gidney Adder
#输出电路图 + 4个指标
import cirq
import mathematics
from mathematics import CarryRipple4TAdder
from utils.counting_utils import *
from qramcircuits.toffoli_decomposition import *

def Craig_Gidney_adder(nr_qubits,c0,aaa,bbb):
    #决定n位加法器
    #nr_qubits = input("请输入一个整数：")
    # python中input函数输出的是一个字符串，而只有通过int进行强制转换
    nr_qubits = int(nr_qubits)

    #构造电路
    c=CarryRipple4TAdder(nr_qubits, use_dual_ancilla = False).construct_circuit(nr_qubits)
    c1=CarryRipple4TAdder(nr_qubits, use_dual_ancilla = False)


    #电路情况
    #print(c.to_text_diagram)#输出每一个Moment所含的gate
    print(c1)#电路图

    #Toffoli分解
    halff = 4*nr_qubits-7

    #compute
    ct=cirq.Circuit(ToffoliDecomposition.construct_decomposed_moments(c.moments[0:halff], ToffoliDecompType.ZERO_ANCILLA_TDEPTH_2_COMPUTE))
    # uncompute
    ct.append(ToffoliDecomposition.construct_decomposed_moments(c.moments[halff:], ToffoliDecompType.ZERO_ANCILLA_TDEPTH_0_UNCOMPUTE))
    qubit_order=CarryRipple4TAdder(nr_qubits, use_dual_ancilla = False).qubit_order
    #print("qubit_order",qubit_order)

    '''
    #分解后电路
    ct_pic=ct.to_text_diagram(use_unicode_characters=False,
                                          qubit_order =qubit_order)
    print(ct_pic)
    #print(ct)
    #T-count、T-depth、Qubit-count、CNOT-count
    print("分解前电路")
    print("T-depth= ", count_t_depth_of_circuit(c))
    print("T-count= ", count_t_of_circuit(c))
    #print("CNOT-count= ", count_cnot_of_circuit(c))
    print("Qubit-count=",len(c.all_qubits()))
    print("Toffoli-count=", count_toffoli_of_circuit(c))

    print("分解后电路")
    print("Qubit-count=", len(ct.all_qubits()))  # 3n-1
    print("T-depth= ", count_t_depth_of_circuit(ct)) #2n-2
    print("T-count= ", count_t_of_circuit(ct))  # 4n-4

    '''

    #print("calculate,由低到高:")
    initial_state = str(c0)
    for i in range(nr_qubits):
        initial_state = initial_state + aaa[i] + bbb[i] + str(0)
    initial_state = initial_state[:-1]
    initial_state = [int(initial_state[i], 2) for i in range(3 * nr_qubits)]
    #simulator
    simulator = cirq.Simulator()
    result1 = simulator.simulate(c,qubit_order=qubit_order,initial_state=initial_state)
    result=str(result1)
    result=result[result.index('|')+1:-1]
    real_result=""
    for i in range(nr_qubits):
        real_result=real_result+result[2+i*3]
    return c1,real_result



if __name__ == "__main__":
    Craig_Gidney_adder(nr_qubits=4,c0=0, aaa="1010", bbb="0101")
