#Quantum Brent-Kung Structure
import cirq
import math
from utils.counting_utils import *

def calculate_Toffoli(circuit):
    Toffoli_depth = count_toffoli_depth_of_circuit(circuit)
    print("Toffoli-depth= ",Toffoli_depth)
    return Toffoli_depth

def BKtree(nr_qubits):

    bitwidth_i = nr_qubits - 1
    #print("bitwidth_i",bitwidth_i)
    if bitwidth_i>0:
        log2_bitwidth = bitwidth_i.bit_length() #math.floor(math.log2(nr_qubits - 1))
    #if bitwidth_i==1:
        #log2_bitwidth=1
    #print("log2_bitwidth",log2_bitwidth)
    tree_matrice =[[i for i in range(bitwidth_i+1)] for j in range(log2_bitwidth * 2)]
    #print(tree_matrice)
    for idx_row in range(log2_bitwidth):
        shift_length = int(math.pow(2,idx_row + 1))  # Shift lenght; Sequence in the loop 2, 4, 8, 16..
        starting_index = shift_length - 2  # Starting indexes in the matrix; Sequence in the loop 0 2 6 14 ...
        starting_value = int(math.pow(2,idx_row) - 1)  # Starting values in the matrix; Sequence in the loop 0 1 3 7 15(shift_length/2 - 1)
        # Mades the row values and indexes sequences
        values_seq = list(range(starting_value, bitwidth_i, shift_length))
        indexes_seq = list(range(starting_index, bitwidth_i, shift_length))
        if not indexes_seq:  # There is no other index
            continue
            # If the root of prefixtree wasnt saved yet. The index (bitwidth) is not power of two.
            # indexes_seq = [bitwidth_i - 1] # Save the right-most index {The index of index -> (-1 -1)}
        # Fill the row
        for index, val in zip(indexes_seq, values_seq):
            tree_matrice[idx_row][index+1] = val
            #print(idx_row,index+1, val)
            #print(tree_matrice)
    """ Creates the inverse tree. 
    bit: 1 2 3 4 5 6 7                   1 2 3 4 5 6 7 
       [[        3    ]     indexes => [[        4    ]  # Start 
        [  1   3   5  ]] <= values      [  1   3   5  ]  # Start 1, shift 2
    """
    for idx_row in range(1, log2_bitwidth + 1):
        shift = 2 ** idx_row  # Sequence  2 4 8 16 32
        values_start = shift - 1  # Sequence 1 3 7 15
        indexes_start = (-4 + 3 * (2 ** idx_row)) // 2  # Sequence 1 4 10 22 46 etc.
        values = range(values_start, bitwidth_i, shift)
        indexes = range(indexes_start, bitwidth_i, shift)
        # Fill the row
        for index, val in zip(indexes, values):

            my_row=log2_bitwidth * 2-idx_row
            #print(my_row, index + 1, val)
            tree_matrice[my_row][index + 1] = val
    return tree_matrice
            # Do not manipulate with idx_row, else it will not be usable for Lander Sklansky and Han Carlson adders


def calculate_P(circuit,p0,p1,p_new):
    circuit.append(cirq.CCNOT(p0,p1,p_new))
    return circuit,p_new
def calculate_G(circuit,g0,p1,g1):
    circuit.append(cirq.CCNOT(g0,p1,g1))
    return circuit, g1

def calculate_PG(circuit,p0,g0,p1,g1,p_new):    #T-depth=2
    circuit,p_new=calculate_P(circuit, p0, p1, p_new) #4 Toffoli
    circuit,g1=calculate_G(circuit, g0, p1, g1) #4 Toffoli
    #Total 5 toffoli
    return circuit

def calculate_Quantum_BKtree(BK_tree,circuit,qubits_p,qubits_g,p_pairs,g_pairs,qubits_p_decomputation,decomputation=False):
    '''
    bitwidth_i = nr_qubits - 1
    log2_bitwidth = math.floor(math.log2(nr_qubits - 1))
    tree_matrice = [[i for i in range(bitwidth_i + 1)] for j in range(log2_bitwidth * 2)]
    '''
    initial_state=""
    _qubit_order=[]
    for i in range(len(qubits_p)):
        _qubit_order.append(qubits_p[i])
        _qubit_order.append(qubits_g[i])
        initial_state = initial_state + p_pairs[i] + g_pairs[i]
    row_len=len(BK_tree)
    if row_len!=0:
        index_len=len(BK_tree[0])
        #print(row_len,index_len)
        for row in range(row_len):
            for index in range(index_len):
                if BK_tree[row][index]!=index:  #不为index,则做PG计算
                    val=BK_tree[row][index]
                    qubits_p_new=cirq.NamedQubit("pnew_" + str(row)+'_'+str(index))
                    _qubit_order.append(qubits_p_new)
                    initial_state = initial_state +"0"
                    circuit=calculate_PG(circuit, qubits_p[val], qubits_g[val], qubits_p[index], qubits_g[index], qubits_p_new)
                    qubits_p[index]=qubits_p_new
    if decomputation!=False:
        row_len = len(BK_tree)
        if row_len != 0:
            index_len = len(BK_tree[0])
            for row in range(row_len):
                for index in range(index_len):
                    if BK_tree[row][index] != index:  # 不为index,则做PG计算
                        val = BK_tree[row][index]
                        qubits_p_new = cirq.NamedQubit("pnew_" + str(row) + '_' + str(index))
                        #_qubit_order.append(qubits_p_new)
                        #initial_state = initial_state + "0"
                        print( "!", qubits_p[val], qubits_p_decomputation[index], qubits_p_new)
                        circuit,p_useless = calculate_P(circuit, qubits_p[val], qubits_p_decomputation[index], qubits_p_new)
                        qubits_p_decomputation[index] = qubits_p_new


        #print(_qubit_order)
    circuit_pic = circuit.to_text_diagram(use_unicode_characters=True,
                                              qubit_order=_qubit_order)
    print(circuit_pic)
    calculate_Toffoli(circuit)
        #print(initial_state)
    #else:
        #print("too small,do nothing")
    return initial_state,_qubit_order,circuit


def Q_BK(cin,p_pairs,g_pairs,decomputation=False):
    #设置cin=0
    nr_qubits=len(p_pairs)-1 #don't need the c_highest_bit
    #print(nr_qubits)


    circuit = cirq.Circuit()
    qubits_p_decomputation = [cirq.NamedQubit("p" + str(i)) for i in range(nr_qubits)]
    qubits_p = [cirq.NamedQubit("p" + str(i)) for i in range(nr_qubits)]
    qubits_g = [cirq.NamedQubit("g" + str(i)) for i in range(nr_qubits)]
    #qubits_p_new = [cirq.NamedQubit("p_new" + str(i)) for i in range(nr_qubits)]
    if nr_qubits>1:
        print("BK")
        BK_tree=BKtree(nr_qubits)
    else:
        print("no BK")
        BK_tree =[]
    print("BK_tree",BK_tree)

    #calculate_PG(circuit, qubits_p[0], qubits_g[0],qubits_p[1], qubits_g[1], qubits_p_new[0])
    #print(circuit)
    initial_state,_qubit_order,circuit=calculate_Quantum_BKtree(BK_tree,circuit,qubits_p,qubits_g,p_pairs,g_pairs,qubits_p_decomputation,decomputation=decomputation)
    c_pairs=''

    #simulator
    simulator = cirq.Simulator()
    initial_state = [int(initial_state[i], 2) for i in range(len(initial_state))]
    result1 = simulator.simulate(circuit,qubit_order=_qubit_order,initial_state=initial_state)
    #print(result1)
    result=str(result1)
    result=result[result.index('|')+1:-1]
    #print(result)

    for i in range(0,nr_qubits):
        #7,6    14,13; 6 5    13 12
        c_pairs = c_pairs + result[2*i+1]
        #print(2*i+1)
        #print((2*radix+1)*i-1,(2*radix+1)*i-1-1)

    return c_pairs#包括c0.。。。c_highest-1


if __name__ == "__main__":
    # p_pairs="101"
    # g_pairs="111"
    # c0=0
    # c_pairs=Q_BK(cin=c0,p_pairs=p_pairs,g_pairs=g_pairs)
    # print(c_pairs)
    c0 = 0
    print("3:")
    c_pairs = Q_BK(cin=c0, p_pairs="101", g_pairs="101",decomputation=False)
    c_pairs = Q_BK(cin=c0, p_pairs="101", g_pairs="101", decomputation=True)

    print("4:")
    c_pairs = Q_BK(cin=c0, p_pairs="1011", g_pairs="1011", decomputation=False)
    c_pairs = Q_BK(cin=c0, p_pairs="1011", g_pairs="1011",decomputation=True)
    '''
    print("5:")
    c_pairs = Q_BK(cin=c0, p_pairs="10111", g_pairs="10111")
    print("6:")
    c_pairs = Q_BK(cin=c0, p_pairs="101110", g_pairs="101110")
    print("7:")
    c_pairs = Q_BK(cin=c0, p_pairs="1011101", g_pairs="1011111")
    print("8:")
    c_pairs = Q_BK(cin=c0, p_pairs="10111111", g_pairs="10111111")
    print("9:")
    c_pairs = Q_BK(cin=c0, p_pairs="101111111", g_pairs="101111111")
    print("10:")
    c_pairs = Q_BK(cin=c0, p_pairs="1011111111", g_pairs="1011111111")
    print("11:")
    c_pairs = Q_BK(cin=c0, p_pairs="10111111111", g_pairs="10111111111")
    '''