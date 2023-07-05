#Compare T depth
import math

def w(x):
    count=0
    while x:
        count+=1
        x&=(x-1)
    return count

def VBE_1(n):
    TD=12*n-6
    print(TD)
def VBE_0(n):
    TD=3*n+4
    print(TD)
def Cucarro_1(n):
    TD=6*n-3
    print(TD)
def Cucarro_0(n):
    TD=n+2
    print(TD)
def Draper_InPlace_1(n):
    TD = 24+3*math.floor(math.log2(n))+3*math.floor(math.log2(n-1))+3 * math.floor(math.log2(n/3)) + 3 * math.floor(math.log2((n - 1)/3))
    print(TD)
def Draper_InPlace_0(n):
    TD = 15 + 3 * math.floor(math.log2(n)) + 3 * math.floor(math.log2(n - 1))+3 * math.floor(math.log2(n / 3)) + 3 * math.floor(math.log2((n - 1) / 3))
    print(TD)
def Draper_Out_of_Place_1(n):
    TD = 12 + 3 * math.floor(math.log2(n)) + 3 * math.floor(math.log2(n/3))
    print(TD)
def Draper_Out_of_Place_0(n):
    TD = 7 + 3 * math.floor(math.log2(n)) + 3 * math.floor(math.log2(n/3))
    print(TD)
def Takahashi_Adder_1(n):
    TD =90*math.log2(n)#?
    print(TD)
def Takahashi_RCA_1(n):
    TD=6*n-3
    print(TD)
def Takahashi_RCA_0(n):
    TD=n+3
    print(TD)
def Takahashi_Combination_1(n):
    TD =54*math.log2(n)#?
    print(TD)
def Gidney_0(n):
    TD=n
    print(TD)#,'&'

# ###########Our Adder(different Toffoli decomposition)################################
def Our_Adder_Method3(n,r):
    TD =6*(math.floor(math.log2(math.ceil(n/r)-1))+math.floor(math.log2(1/3*(math.ceil(n/r)-1)))+4)+math.floor(6*math.log2(r-2)+1)+9*r-10
    print(TD)
def Our_Adder_Gidney_Method3(n,r):
    TD = 6 * (math.floor(math.log2(math.ceil(n / r) - 1)) + math.floor(math.log2(1 / 3 * (math.ceil(n / r) - 1))) + 4) + math.floor(6 * math.log2(r - 2) + 1) + 7* r - 7
    print(TD)
def Our_Adder_LogicalAnd_Method3(n,r):
    TD =6*(math.floor(math.log2(math.ceil(n/r)-1))+math.floor(math.log2(1/3*(math.ceil(n/r)-1)))+4)+math.floor(math.log2(r-2)+1)+2*r-6
    print(TD)
if __name__ == "__main__":
    ##############################
    print("VBE_RCA!")
    bit=8
    for i in range(7):
        bit=2*bit
        VBE_1(bit)
    print("VBE_RCA@")
    bit=8
    for i in range(7):
        bit=2*bit
        VBE_0(bit)
    ###############################
    print("Cucarro_RCA!")
    bit = 8
    for i in range(7):
        bit=2*bit
        Cucarro_1(bit)
    print("Cucarro_RCA@")
    bit = 8
    for i in range(7):
        bit=2*bit
        Cucarro_0(bit)
    ##############################
    print("Draper In-place CLA!")
    bit = 8
    for i in range(7):
        bit=2*bit
        Draper_InPlace_1(bit)
    print("Draper In-place CLA@")
    bit = 8
    for i in range(7):
        bit=2*bit
        Draper_InPlace_0(bit)
    ##############################
    print("Draper Out-of-place CLA!")
    bit = 8
    for i in range(7):
        bit=2*bit
        Draper_Out_of_Place_1(bit)
    print("Draper Out-of-place CLA@")
    bit = 8
    for i in range(7):
        bit=2*bit
        Draper_Out_of_Place_0(bit)
    ##############################
    print("Takahashi Adder!")
    bit = 8
    for i in range(7):
        bit=2*bit
        Takahashi_Adder_1(bit)
    ###############################
    print("Takahashi_RCA!")
    bit = 8
    for i in range(7):
        bit=2*bit
        Takahashi_RCA_1(bit)

    print("Takahashi_RCA@")
    bit = 8
    for i in range(7):
        bit=2*bit
        Takahashi_RCA_0(bit)
    ###############################
    print("Takahashi Combination!")
    bit = 8
    for i in range(7):
        bit=2*bit
        Takahashi_Combination_1(bit)
    ###############################
    print("Gidney@")
    bit = 8
    for i in range(7):
        bit=2*bit
        Gidney_0(bit)
    ############################################################
    ###########################
    print("Our Adder!")
    bit = 8
    r=9
    for r in range(3,16):
        print("r=",r)
        bit = 8
        for i in range(7):
            bit = 2 * bit
            Our_Adder_Method3(bit, r)
    ################################
    print("Our Adder(Method3 & Gidney)")
    for r in range(3,16):
        print("r=",r)
        bit = 8
        for i in range(7):
            bit = 2 * bit
            Our_Adder_Gidney_Method3(bit,r)
    ################################
    # print("Our Adder@")
    # bit = 8
    # for r in range(3,16):
    #     print("r=",r)
    #     bit = 8
    #     for i in range(7):
    #         bit = 2 * bit
    #         Our_Adder_LogicalAnd_Method3(bit,r)



