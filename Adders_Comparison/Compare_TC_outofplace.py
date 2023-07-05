#Compare T count(out of place adder)
import math

def w(x):

    count=0
    while x:
        count+=1
        x&=(x-1)
    return count

def VBE_1(n):
    TC=28*n-14
    print(TC)
def VBE_0(n):
    TC=8*n+6
    print(TC)
def Cucarro_1(n):
    TC=14*n-7
    print(TC)
def Cucarro_0(n):
    TC=4*n+3
    print(TC)

def Draper_InPlace_1(n):
    TC =70*n-21*w(n)-21*w(n-1)-21*math.floor(math.log2(n))-21*math.floor(math.log2(n-1))-49
    print(TC)
def Draper_InPlace_0(n):
    TC =50*n-11*w(n)-21*w(n-1)-11*math.floor(math.log2(n))-21*math.floor(math.log2(n-1))-39
    print(TC)
def Draper_Out_of_Place_1(n):
    TC = 35*n-21*w(n)-21*math.floor(math.log2(n))-7
    print(TC)
def Draper_Out_of_Place_0(n):
    TC = 25*n-11*w(n)-11*math.floor(math.log2(n))-7
    print(TC)

def Takahashi_Adder_1(n):
    TC =196*n#?
    print(TC)
def Takahashi_RCA_1(n):
    TC=14*n-7
    print(TC)
def Takahashi_RCA_0(n):
    TC=4*n+3
    print(TC)
def Takahashi_Combination_1(n):
    TC =49*n
    print(TC)
def Gidney_0(n):
    TC=4*n-4
    print(TC)#,'&'

# ###########Our Adder################################
def Our_Adder_Method3(n,r):
    TC =(35*r-7)*math.ceil(n/r)+21*n-7*((n-1)%r)-35-35*r-21*w(math.ceil(n/r)-1)-21*(math.floor(math.log2(math.ceil(n/r)-1)))
    #remove BK-1
    TC=TC-7*(2*(math.ceil(n/r)-1)-1-w(math.ceil(n/r)-1)-math.floor(math.log2(math.ceil(n/r)-1)))
    #remove higer radix-1
    TC=TC-7*(math.ceil(n/r)-1)*(r-2+r-1)
    #remove Gidney-1
    TC=TC-7*(n-math.ceil(n/r))
    #print(TC)
    return TC
def Our_Adder_Gidney_Method3(n,r):
    TC =(35*r+3)*math.ceil(n/r)+11*n-7*((n-1)%r)-35-35*r-21*w(math.ceil(n/r)-1)-21*(math.floor(math.log2(math.ceil(n/r)-1)))
    #remove BK-1
    TC=TC-7*(2*(math.ceil(n/r)-1)-1-w(math.ceil(n/r)-1)-math.floor(math.log2(math.ceil(n/r)-1)))
    #remove higer radix-1
    TC=TC-7*(math.ceil(n/r)-1)*(r-2+r-1)
    #print(TC)
    return TC
def Our_Adder_LogicalAnd_Method3(n,r):
    TC =(8*r+40)*math.ceil(n/r)+11*n-7*((n-1)%r)-72-8*r-21*w(math.ceil(n/r)-1)-21*(math.floor(math.log2(math.ceil(n/r)-1)))
    #remove BK-1
    TC=TC-7*(2*(math.ceil(n/r)-1)-1-w(math.ceil(n/r)-1)-math.floor(math.log2(math.ceil(n/r)-1)))
    #print(TC)
    return TC

if __name__ == "__main__":
    # #############################
    # print("VBE_RCA!")
    # bit=8
    # for i in range(7):
    #     bit=2*bit
    #     VBE_1(bit)
    # print("VBE_RCA@")
    # bit=8
    # for i in range(7):
    #     bit=2*bit
    #     VBE_0(bit)
    # ###############################
    # print("Cucarro_RCA!")
    # bit = 8
    # for i in range(7):
    #     bit=2*bit
    #     Cucarro_1(bit)
    # print("Cucarro_RCA@")
    # bit = 8
    # for i in range(7):
    #     bit=2*bit
    #     Cucarro_0(bit)
    # #############################
    # print("Draper In-place CLA!")
    # bit = 8
    # for i in range(7):
    #     bit=2*bit
    #     Draper_InPlace_1(bit)
    # print("Draper In-place CLA@")
    # bit = 8
    # for i in range(7):
    #     bit=2*bit
    #     Draper_InPlace_0(bit)
    # ###############################
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
    # #############################
    # print("Takahashi Adder!")
    # bit = 8
    # for i in range(7):
    #     bit=2*bit
    #     Takahashi_Adder_1(bit)
    # ###############################
    # print("Takahashi_RCA!")
    # bit = 8
    # for i in range(7):
    #     bit=2*bit
    #     Takahashi_RCA_1(bit)
    #
    # print("Takahashi_RCA@")
    # bit = 8
    # for i in range(7):
    #     bit=2*bit
    #     Takahashi_RCA_0(bit)
    # ###############################
    # print("Takahashi Combination!")
    # bit = 8
    # for i in range(7):
    #     bit=2*bit
    #     Takahashi_Combination_1(bit)
    # ###############################
    # print("Gidney@")
    # bit = 8
    # for i in range(7):
    #     bit=2*bit
    #     Gidney_0(bit)
    #############################################################
    ############################
    print("Our Adder!")
    bit = 1024
    list1=[]
    list2=[]
    list3=[]
    for r in range(3,bit):
        #print("r=",r)
        list1.append(Our_Adder_Method3(bit, r))
    print(min(list1))
    ################################
    print("Our Adder(Method3 & Gidney)")
    for r in range(3,bit):
        #print("r=",r)
        list2.append(Our_Adder_Gidney_Method3(bit,r))
    print(min(list2))
    ################################
    print("Our Adder@")
    for r in range(3,bit):
        #print("r=",r)
        list3.append(Our_Adder_LogicalAnd_Method3(bit,r))
    print(min(list3))


