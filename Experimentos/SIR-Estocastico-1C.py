#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sun Jul 19 07:01:51 2020

@author: fernando
"""

def SIR_2C_estocastico(N,n,R):
    """
    Dos ciudades sobre las que avanza una epidemia. En cada una de ellas se
    asume un modelos SIR discreto. Se asume que en cada iteración con 
    probabilidad p un individuo de una ciudad puede pasar a la otra.
    La primera ciudad con un número de reproducción básico R01 y la segunda 
    con R02. La unidad de tiempo es el periodo de infectividad y la población
    total está normalizada N=1.
    Parametros:
        n: int (#iteraciones)
        R01: float64,  número de reproducción básico ciudad 1
        R02: float64,  número de reproducción básico ciudad 2
        p: float64, probabilidad que se intercambie Delta_H habitantes
           entre ciudades
        Delta_H: float 64 algo así como un individuo
    """
    
    x0=np.array([N-1, 1, 0],dtype=int)
    
    ## delta_s son los incrementos de tiempos. 
    ##Debe ser elegido
    ##               delta_s<min{1,1/max{R01,R02}}
    
    beta=R0/N
    
    delta_s=.5*min(1,1.0/beta)
    
    X=np.zeros([3,n],dtype=int)
    X[:,0]=x0
    for i in range(n-1):
        X[:,i+1]=SIR_est_2C(X[:,i],beta,delta_s)
    return X



def SIR_est_2C(x,beta, delta_s):
    
    ## Decidir cuantos habitantes pasan de una población a otra
    S,I,R=x
    
    
    #r=rand(3)
        
    Id=poisson(lam=beta*delta_s*S*I)
    Id=min(Id,S)
    Rd=poisson(lam=delta_s*I)
    Rd=min(Rd,I)
    
    S_new=S-Id
    I_new=I-Rd+Id
    R_new=R+Rd
    
    X=np.array([S_new,I_new,R_new])
    return X




from numpy.random import poisson


###################  EXPERIMENTO #############################################
##############################################################################




R0=2.0
N=10000
delta_s=.1*min(1,N/R0)
iteraciones=100


X=SIR_2C_estocastico(N,iteraciones,R0)

n,j=np.shape(X)
s=np.arange(0,j*delta_s,delta_s)


fig, ax = plt.subplots(figsize=(10,16))

ax.plot(s,X.T)
ax.set_title('Ciudad 1')
