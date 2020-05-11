#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Thu May  7 08:13:53 2020

@author: fernando
"""


import numpy as np
from scipy.integrate import odeint 
import matplotlib.pyplot as plt
import scipy.optimize


def SIR(Y,t,params):
    R0=params[0]
    
    #S,I,R=Y[0],Y[1],Y[2]
    dSds=-R0*Y[0]*Y[1]
    dIds=R0*Y[0]*Y[1]-Y[1]
    dRds=Y[1]
    return dSds,dIds,dRds
####### Resolvemos el modelos
def SEIR(Y,t,params):
    R0,k_ast=params
    #S,I,R,E=Y
    dSds=-R0*Y[0]*Y[1]
    dIds=k_ast*Y[3]-Y[1]
    dRds=Y[1]
    dEds=R0*Y[0]*Y[1]-k_ast*Y[3]
    return dSds,dIds,dRds,dEds

def Modelo(nombre):
    switcher = {
        'SIR': SIR,
        'SEIR': SEIR
    }
    func = switcher.get(nombre, lambda: "Modelo No implementado")
    return func
"""
Y0=[254,7,0]
t = np.linspace(0,30, 1000)
argus=((2.73, 0.017),)
f=Modelo('SIRD')
sol = odeint(f,Y0 ,t, args=argus)
S,I=sol[:,0],sol[:,1]
plt.plot(t,I)
plt.show()
"""


def Error(x,*params):
    Metodo,Data=params
    #x[0]=alpha, x[1]=R0, x[2:]=otros param
    #Cambio escala tiempo
    s=np.arange(np.shape(Data)[0])*x[0]  
    Y0=Data[0,:] #Condicion Inicial
    f=Modelo(Metodo)
    Sol = odeint(f,Y0 ,s, args=(x[1:],))
    #M=Poblacion-Sol[:,0]-Sol[:,1]-Sol[:,2]
    #Data=[S,I,R,M,Iacum]
    return sum(np.abs(Data[:,1]-Sol[:,1])**2)
#max(np.abs(Data[:,1]-Sol[:,1]))

#max(np.abs(Data[:,1]-Sol[:,1]))
#/(max(I_data)+1)\
#+max(np.abs(S_data-S))/(max(S_data)+1)+max(np.abs(R_data-R))/(max(R_data)+1)\
#+max(np.abs(M_data-M))/(max(M_data)+1)

def OptBruto(Data,Poblacion,Metodo,rangos):
    opt=scipy.optimize.brute(Error,rangos,args=(Metodo,Data0),finish=None,full_output=True)
    para_opt,feval=opt[0:2]
    return para_opt,feval

def OptMinimize(Data,Metodo,rangos):
    param0=np.array([.5*sum(i) for i in rangos])
    argu=(Metodo,Data)
    para_opt= scipy.optimize.minimize(Error,param0,args=argu,method='L-BFGS-B', bounds=rangos)
    return para_opt