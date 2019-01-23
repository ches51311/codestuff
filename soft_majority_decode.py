import numpy as np
from math import factorial
from itertools import combinations
import random
from time import time

def perm(n, m):
    return(factorial(n) / factorial(n - m))

def comb(n, m):
    return(perm(n, m) / factorial(m))

#generate reed muller matrix
def Reed_Muller_matrix(r,m):
    row = 0
    for i in range(r+1):
        row = row + comb(m,i)

    M = np.zeros((row, pow(2,m)))

    num = 0
    for i in range(r+1):
        for L in list(combinations(range(1,m+1), i)):
            for k in range(pow(2,m)):
                if len(L) == 0:
                    M[num][k] = 1
                if len(L) == 1:
                    M[num][k] = (k/pow(2,m-L[0])%2)
            if len(L) > 1:
                M[num] = M[0]
                for x in L:
                    M[num] = M[num] * M[x]

            num = num + 1
    return M

#ex, in RM(2,4), the sixth row is made by x1 and x2
def row_of_combination(r,m):
    x_multi = {}
    i=0
    for j in range(r+1):
        for L in list(combinations(range(1,m+1), j)):
            x_multi[i]=L
            i=i+1
    return x_multi

def specific_len(x_multi, order):
    x_multi_r = {}
    for i in x_multi:
        if len(x_multi[i]) == order:
            x_multi_r[i]=x_multi[i]
    return x_multi_r



#int to binary
def i2b(ii,m):
    a=[]
    for j in range(m):
        a.append(ii%2)
        ii = ii/2
    a.reverse()
    return a

#ex, m=4 is [1,2,3,4], and place=[3,4] mean return 
def same_xj(m,place):
    place2 = range(1,m+1)
    place = list(set(place2).difference(set(place)))
    place = [p-1 for p in place]
    xja=[]
    Xj=[]

    for i in range(pow(2,len(place))):
        for j in range(pow(2,m)):
            check = True
            for k in range(len(place)):
                if i2b(j,m)[place[k]] != i2b(i,len(place))[k]:
                    check = False
            if check == True:
                xja.append(j)
        if Xj==[]:
            Xj=np.array([xja])
        else:
            Xj=np.append(Xj,[xja], axis=0)
        xja=[]
    return Xj










def random_information_bits(row):
    U = np.zeros(row)    
    for i in range(row):
        U[i] = int(random.randint(0,1))
    return U



def reed_muller_encode(U, RM):
    V = np.zeros(pow(2,m))
    for i in range(pow(2,m)):
        V[i] = sum(U*RM[:,i]) % 2
    return V


def send_channel(V, sigma):
    for i in range(len(V)):
        if V[i]==1:
            V[i]=-1
        if V[i]==0:
            V[i]=1
        V[i] = V[i] + np.random.normal(loc=0.0, scale=sigma, size=None)
    return V
    


def soft_majority_decode(V, r, m, RM, x_multi, row, column, sigma):

    #turn to tanh(2*ux/sigma^2)
    for i in range(len(V)):
        V[i] = np.tanh(2*V[i]/(sigma*sigma))
    #print V



    ans=np.zeros(row)
    for a in range(len(ans)):
        ans[a]=-2


    for order in range(r,0,-1):
        x_multi_r = specific_len(x_multi, order)
        next_order_site = max(x_multi_r)+1
        for i in x_multi_r:
            Aj=[]
            Xj = same_xj(m,x_multi_r[i])
            for xja in Xj:
                xmul = 1
                for z in xja:
                    xmul = xmul * V[z]
                

                for z in xja:
                    for ii in range(next_order_site,row):
                        if RM[ii,z] == 1:
                            xmul = xmul*ans[ii]
                Aj.append(xmul)

            if sum(Aj) >= 0:
                ans[i]=1
            if sum(Aj) < 0:
                ans[i]=-1

    
# ???
    ss = 1
    for i in range(1, len(ans)):
        ss = ss * ans[i]
    ss = ss * V[len(V)-1]
#    ss = (sum(ans[1:])+V[len(V)-1]) % 2
    if ss >=0:
        ans[0] = 1
    if ss < 0:
        ans[0] = -1

    return ans



if __name__ == "__main__":

#    r=3
    r=1
    m=5
    SNR=2
    iteration=1000000000
    sub_iter= 50000000
#    iteration=1000
#    sub_iter= 50

    num_iter = iteration/sub_iter

    RM = Reed_Muller_matrix(r,m)
    x_multi = row_of_combination(r,m)
    row = len(RM[0:])
    column = len(RM[0])
    R=float(row)/float(column)
    sigma = 1/(2*R*SNR)
    sigma = sigma**0.5

    t_spend = []
    BlER = []
    BER = []    

    for t1 in range(num_iter):
        t_start = time()
        BER1=0
        BlER1=0
        for t2 in range(sub_iter):
            U = random_information_bits(row)
            V = reed_muller_encode(U, RM)
            V = send_channel(V, sigma)
            U_ans = soft_majority_decode(V, r, m, RM, x_multi, row, column, sigma)
            for i in range(len(U)):
                if U[i]==1:
                    U[i]=-1
                if U[i]==0:
                    U[i]=1
            BER1 = BER1 + sum(abs(U-U_ans)/2)
            if sum(abs(U-U_ans)) > 0:
                BlER1 = BlER1 + 1
        t_end = time()
        t_spend1 = t_end - t_start
        BlER1 = float(BlER1)/float(sub_iter)
        BER1 = float(BER1)/float(sub_iter*row)
        t_spend.append(t_spend1)
        BlER.append(BlER1)
        BER.append(BER1)
        print "iter num = ", t1+1
        print "Simu_time = ", t_spend1
        print "Block_error_rate = ", BlER1
        print "Bit_error_rate = ", BER1
        print ""


    print "\n\nTotal Simu_time = ", sum(t_spend)
    print "SNR = ", SNR
    print "Total Block_error_rate = ", sum(BlER)/len(BlER)
    print "Total Bit_error_rate = ", sum(BER)/len(BER)

    with open("sim_out.txt", "w") as f:

        f.write("r=")
        f.write(str(r))
        f.write("\n")

        f.write("m=")
        f.write(str(m))
        f.write("\n")

        f.write("SNR=")
        f.write(str(SNR))
        f.write("\n")

        f.write("iteration=")
        f.write(str(iteration))
        f.write("\n")

        f.write("sub_iter=")
        f.write(str(sub_iter))
        f.write("\n")

        f.write("num_iter=")
        f.write(str(num_iter))
        f.write("\n")

        f.write("Simu_time=")
        f.write(str(t_spend))
        f.write("\n\n")

        f.write("Block_error_rate=")
        f.write(str(BlER))
        f.write("\n\n")

        f.write("Bit_error_rate=")
        f.write(str(BER))
        f.write("\n")

