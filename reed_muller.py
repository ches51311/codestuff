import numpy as np
from math import factorial
from itertools import combinations
import random


def perm(n, m):
    return(factorial(n) / factorial(n - m))

def comb(n, m):
    return(perm(n, m) / factorial(m))

def binary(m):
    A = np.zeros((pow(2,m),m))
    for i in range(pow(2,m)):
        n=i
        for j in range(m-1,-1,-1):
            A[i][m-1-j] = n/pow(2,j)
            n = n%pow(2,j)
    return A



def RM(r,m):
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

def parity_check(r,m,N):
    M = RM(r,m)
    
    row = 0
    for i in range(r+1):
        row = row + comb(m,i)
    U = np.zeros(row)
    V = np.zeros(pow(2,m))

    for i in range(row):
        U[i] = random.randint(0,1)
    for i in range(pow(2,m)):
        V[i] = sum(U*M[:,i]) % 2
        a=1



    print V






M = RM(2,4)
#print M
#parity_check(2,4,10)
print binary(6)