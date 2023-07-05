# 64 bits quantum high radix adder
import cirq
import mathematics
import random
import Craig_Gidney
from AdderExample.HigherRadixAdder_Components.Q_BrentKung import Q_BK
from AdderExample.HigherRadixAdder_Components.Q_high_radix_layer import High_radix_layer
from AdderExample.HigherRadixAdder_Components.Quantum_MUX import Q_MUX
from AdderExample.HigherRadixAdder_Components.Quantum_pg import Q_pg
import math

'''
Since the whole circuit is kind of too big, this program uses several subcircuits to complete the calculation.

It's nonsense to implement the part 5 and part 6 in the code.

But to better understand the overall design,
You can go to the corresponding sub-function to see the detailed design. :)
'''
def Quantum_High_Radix(add_bit_num,radix_num):
    CSA_bits = radix_num


    '''part0: preprocessing
    low->high, random generate addends a and b  
    example:(low)001011(high)
    '''
    a=''.join(str(random.randint(0, 1)) for _ in range(add_bit_num))
    b= ''.join(str(random.randint(0, 1)) for _ in range(add_bit_num))
        #''.join(str(0) for _ in range(add_bit_num) )
    print("a,b: ",a,b)



    '''part1: calculate p and g
    based on a and b.
    '''
    p, g=Q_pg(nr_qubits=add_bit_num,a=a,b=b)
    print("p,g: ",p,g)



    '''part2: 1 higher radix layer
    based on p and g, calculate p_pairs and g_pairs.
    
    min(radix_num) = 2
    max(radix_num) < add_bit_num
    
    if radix_num==1, 
    higher radix adder == Draper's inplace CLA adder
    
    if radix_num==add_bit_num, 
    higher radix adder == Gidney's RCA adder
    '''
    p_pairs,g_pairs=High_radix_layer(nr_qubits=add_bit_num,radix=radix_num,p=p,g=g)
    print("p_pairs,g_pairs: ", p_pairs,g_pairs)

    '''part3: (Carry_path)Brent-Kung tree
    based on p_pairs and g_pairs, do the propagation.
    get the carries of different pairs
    
    we don't need the highest carry
    the first carry is always 0.
    '''

    '''part4: (Carry_path)Brent-Kung tree decomputation
    carries are stored in g_pairs.
    So we only decompute the p_pairs

    c_pairs=Q_BK(cin=0,p_pairs=p_pairs,g_pairs=g_pairs,decomputation=True)
    '''

    c_pairs=Q_BK(cin=0,p_pairs=p_pairs,g_pairs=g_pairs,decomputation=True)#除去 c_最高位，c0为0
    c_pairs='0'+c_pairs#把c0添加进去
    print("c0+c_pairs: ", c_pairs)


    '''part5: decomputate part 2
    decomputate p(the multi-control toffoli)
    and (radix-2) g
    '''

    '''part6: decomputate part 1:
    restore a and b
    
    you can go to Quantum_pg.py
    use "Q_pg_decomputation(nr_qubits=4, a="1011", b="0001",radix_num=3)" to check the detailed design.
    '''

    '''part7: (Sum_path)Craig Gidney Adder
    based on p_pairs and g_pairs, do the propagation.
    get the carries of different pairs
    
    final_summ is the final result (Order: low->high)
    '''
    final_summ=''
    for i in range(math.floor(add_bit_num/radix_num)):
        #0:radix,radix:2*radix,2*radix:3*radix
        aaa=a[(i*radix_num):((i+1)*radix_num)]
        bbb=b[(i*radix_num):((i+1)*radix_num)]
        print("i",i)
        print("aaa,bbb: ",aaa,bbb)
        print("RCA_bits", CSA_bits, "c_pairs[i]", c_pairs[i])
        c0_Craig_Gidney,s0=Craig_Gidney.Craig_Gidney_adder(nr_qubits=CSA_bits, c0=c_pairs[i], aaa=aaa, bbb=bbb) #Sum path
        print("s0",s0)
        summ =s0
        final_summ =final_summ+summ
        print("summ",summ)
    print("final_summ",final_summ)

    #MUX->summ

if __name__ == "__main__":


    '''
    How to use the main function
    '''
    print("add_bit_num=6,radix_num=3")
    Quantum_High_Radix(add_bit_num=6,radix_num=2)
    print("Build successfully!")
    #
    # print("add_bit_num=8, radix_num=4")
    # Quantum_High_Radix(add_bit_num=8, radix_num=4)
    # print("")

    # print("add_bit_num=8, radix_num=2")
    # Quantum_High_Radix(add_bit_num=8, radix_num=2)

    # print("add_bit_num=8, radix_num=2")
    # Quantum_High_Radix(add_bit_num=8, radix_num=2)