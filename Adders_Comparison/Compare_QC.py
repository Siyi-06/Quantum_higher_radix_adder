#Compare qubit cost
import math

def w(x):
    count=0
    while x:
        count+=1
        x&=(x-1)
    return count

def VBE(n):
    Qubit=3*n+1
    print(Qubit)
def Cucarro(n):
    Qubit=2*n+2
    print(Qubit)
def Draper_InPlace(n):
    Qubit = 4 * n -w(n)-math.floor(math.log2(n))
    print(Qubit)
def Draper_Out_of_Place(n):
    Qubit = 4 * n +1 -w(n)-math.floor(math.log2(n))
    print(Qubit)
def Takahashi_Adder(n):
    Qubit =2*n+math.floor(3*n/(math.log2(n)))#?
    print(Qubit)
def Takahashi_RCA(n):
    Qubit=2*n+1
    print(Qubit)
def Takahashi_Combination(n):
    Qubit =2*n+math.floor(3*n/(math.log2(n)))#?
    print(Qubit)
def Gidney(n):
    Qubit=3*n-1
    print(Qubit)#,'&'

#Our Adder
def Our_Adder_Method3(n,r):
    Qubit =3*n-w(math.ceil(n/r)-1)+(r+1)*math.ceil(n/r)-math.floor(math.log2(math.ceil(n/r)-1))-3-r
    print(Qubit)
def Our_Adder_Gidney_Method3(n,r):
    Qubit =3*n-w(math.ceil(n/r)-1)+(r+1)*math.ceil(n/r)-math.floor(math.log2(math.ceil(n/r)-1))-3-r
    print(Qubit)
def Our_Adder_LogicalAnd_Method3(n,r):
    Qubit =3*n-w(math.ceil(n/r)-1)+(2*r-1)*math.ceil(n/r)-math.floor(math.log2(math.ceil(n/r)-1))-1-2*r
    print(Qubit)
if __name__ == "__main__":
    bit=8; # 8 bit addition
    r=3;# radix = 3
    ###############################
    print("VBE_RCA")
    VBE(bit)
    ###############################
    print("Cucarro_RCA")
    Cucarro(bit)
    ###############################
    print("Draper In-place CLA")
    Draper_InPlace(bit)
    ###############################
    print("Draper Out-of-place CLA")
    Draper_Out_of_Place(bit)
    ###############################
    print("Takahashi Adder")
    Takahashi_Adder(bit)
    ###############################
    print("Takahashi_RCA")
    Takahashi_RCA(bit)
    ###############################
    print("Takahashi Combination")
    Takahashi_Combination(bit)
    ###############################
    print("Gidney")
    Gidney(bit)
    ############################################################
    print("Our Adder!")
    Our_Adder_Method3(bit, r)
    ################################
    print("Our Adder(Method3 & Gidney)")
    Our_Adder_Gidney_Method3(bit,r)
    ################################
    # print("Our Adder@")
    # Our_Adder_LogicalAnd_Method3(bit,r)




