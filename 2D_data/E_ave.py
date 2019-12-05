import pandas as pd 
import numpy as np
import matplotlib.pyplot as plt 
import random
from scipy.optimize import curve_fit
import math
from tqdm import tqdm
import pandas as pd
import csv

import random, math, numpy as np, os

def energy(S, N, nbr):
    E = 0.0
    for k in range(N):
        E -=  S[k] * sum(S[nn] for nn in nbr[k])
    return 0.5 * E

def magnetization (S, N, nbr):
    M = 0.0
    for k in range(N):
        M += S[k]
    return M



def calculate(S,T,replace=True):
    E = [energy(S, N, nbr)]
    M = [magnetization (S, N, nbr)]
    for step in range(nsteps):
        print(step)
        k = random.randint(0, N - 1)
        Pocket, Cluster = [k], [k]
        while Pocket != []:
            j = random.choice(Pocket) if replace else Pocket.pop()
            for l in nbr[j]:
                if S[l] == S[j] and l not in Cluster \
                       and random.uniform(0.0, 1.0) < p:
                    Pocket.append(l)
                    Cluster.append(l)
            if replace: Pocket.remove(j)
        for j in Cluster:
            S[j] *= -1
        E.append(energy(S, N, nbr))
        M.append(magnetization(S, N, nbr))
    E_mean = sum(E) / len(E)/N
    E2_mean = sum(a ** 2 for a in E) / len(E)/N
    cv = (E2_mean - E_mean ** 2 ) / T ** 2    
    
    M_mean = sum(abs(a) for a in M) / len(M)/N
    M2_mean = sum(a ** 2 for a in M) / len(M)/N
    chi = (M2_mean - M_mean ** 2 ) / T 
    
    return S,E_mean, E2_mean,cv,M_mean, M2_mean,chi

L = 20
N1 = L
N2 = L*L
N = L*L*L

count=0
three_D_chain = []
for k in range(N1):
    two_D_chain = []
    for j in range(N1):
        
        chain = [i+ count*N1 for i in range(N1)]
        chain.append(chain[0])
        chain.append(chain[-2])
        two_D_chain.append(chain)
        count+=1
    two_D_chain.append(two_D_chain[0])
    two_D_chain.append(two_D_chain[-2])
    
    
    three_D_chain.append(two_D_chain)
    
    
    
three_D_chain.append(three_D_chain[0])
three_D_chain.append(three_D_chain[-2])

count=0
nbr = {}
for i in range(N1):
    for j in range(N1):
        for k in range(N1):
            nbr[count]=(three_D_chain[i][j+1][k],three_D_chain[i][j-1][k],three_D_chain[i+1][j][k],three_D_chain[i-1][j][k], \
                   three_D_chain[i][j][k+1],three_D_chain[i][j][k-1])
            count+=1

chi_list = []
M_list = []
cv_list = []
E_list = []
for T in [0.1,1.0,2.0,3.0,3.5,4.0,4.2,4.4,4.5,4.6,4.8,5.0,5.2,5.4,5.6,5.8,6.0,6.2,6.4,6.6,6.8,7.0,8.0,9.0]:
    print(T)
    p  = 1.0 - math.exp(-2.0 / T)
    nsteps = 2000

    S = [random.choice([1, -1]) for k in range(N)]
        #print ('Starting from a random configuration')
    S,E_mean, E2_mean,cv,M_mean, M2_mean,chi=calculate(S,T)
    #chi_list.append(chi)
    #M_list.append(M_mean)
    print(M_mean,chi)
    cv_list.append(cv)
    E_list.append(E_mean)
    M_list.append(M_mean)
    chi_list.append(chi)

with open('cv.csv', 'w', newline='') as myfile:
     wr = csv.writer(myfile)
     wr.writerow(cv_list)


with open('E.csv', 'w', newline='') as myfile:
     wr = csv.writer(myfile)
     wr.writerow(E_list)


with open('M.csv', 'w', newline='') as myfile:
     wr = csv.writer(myfile)
     wr.writerow(M_list)


with open('chi.csv', 'w', newline='') as myfile:
     wr = csv.writer(myfile)
     wr.writerow(chi_list)