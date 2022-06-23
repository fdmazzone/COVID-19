#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jun 12 07:28:42 2021

@author: fernando
"""

import matplotlib.pyplot as plt
from scipy.integrate import odeint 
import numpy as np
from numpy import linalg as LA
from scipy import optimize
from numba import jit  # compila funciones
import time
from multiprocessing import Pool
from scipy.interpolate import UnivariateSpline as spline
#from scipy.integrate import simps



start_time = time.time()
#Poblacion total
N=200000



#################  parte modificable ####################
#Otros Parametros
gamma=1
#R0 y beta
R0=np.array([[1.3,0.1],[.1,1.3]])

#Provición de vacunas
sigmaT=lambda t: .01  
sigmaT = np.vectorize(sigmaT)
#t final
T=50.0 
#Condicion inicial
x0=np.array([.95*N,.05*N,1.0,1.0,2.0])#Pobl1,Pobl2,I1,I2,costo(0)=O

beta=R0*np.array([[1/x0[0], 1/x0[1] ],[1/x0[0],1/x0[1]]])*gamma


#discretizamos el tiempo para el problema minimizacion
t_int=np.linspace(0,T,30)
##########################################################


#@jit(nopython=True)
def SIR2p(x,t,u):
    S,I=x[:2],x[2:4]
    Incidencia=S*beta.dot(I)
    U=np.array([u(t),sigmaT(t)-u(t)])
    dS=-S*U-Incidencia
    dI=-gamma*I+Incidencia
    dJ=gamma*np.sum(I)
    return np.concatenate((dS,dI,[dJ]))


#Función objetivo
def J(U,t):
    u_func=spline(t_int, U,s=0, k=1)
    sol = odeint(SIR2p,x0 ,t,args=(u_func,))
    return sol[-1,4]



############# minimizacion #######################
rangos=[(0,sigmaT(i)) for i in t_int]
t=np.linspace(0,T,100)
opt=optimize.differential_evolution(J,rangos,args=(t,),workers=8)
#opt=optimize.minimize(J, 1.0*sigmaT(t_int) ,bounds=rangos,args=(t,))
##  Control optimo en los puntos t_int



U=opt["x"]



u_func=spline(t_int, U,s=0, k=1)


################Graficamos solucion ##################


sol = odeint(SIR2p,x0 ,t,args=(u_func,))
S=sol[:,:2]
I=sol[:,2:4]
J_val=sol[:,4]


fig,  ((ax1, ax2, ax3),( ax4, ax5, ax6),( ax7, ax8, ax9))=plt.subplots(3,3)
ax1.plot(t,S) #susceptibles
ax1.legend((r'$S_1$',r'$S_2$'))
ax2.plot(t,I)#infeccionsos
ax2.legend((r'$I_1$',r'$I_2$'))
ax3.plot(t,np.sum(I,1)) #suma infecciosos
ax3.legend((r'$I_1+I_2$',))
#control total y u1  u2
ax4.plot(t,np.array([u_func(t),sigmaT(t)-u_func(t),sigmaT(t)]).T)#
ax4.legend((r'$\sigma_1(t)$',r'$\sigma_2(t)$',r'$\sigma_T(t)$'))


################### PROBLEMA ADJUNTO  ###################33

S1=spline(t,S[:,0],s=0)
S2=spline(t,S[:,1],s=0)
I1=spline(t,I[:,0],s=0)
I2=spline(t,I[:,1],s=0)

S_func=lambda t: np.array([S1(t),S2(t)])
I_func=lambda t: np.array([I1(t),I2(t)])

x_func=lambda t: np.array([S1(t),S2(t),I1(t),I2(t)])

def ADJ(lam,t):
    betaI=beta.dot(I_func(T-t))
    U=np.array([u_func(T-t),sigmaT(T-t)-u_func(T-t)])  
    dlam1=betaI*(lam[:2]-lam[2:])+U*lam[:2]
    dlam2=(beta.T).dot(S_func(T-t)*(lam[:2]-lam[2:]))+gamma*lam[2:]+gamma*np.ones(2)
    return np.concatenate((-dlam1,-dlam2)) 

sol = odeint(ADJ, np.zeros(4) ,t)
lam=sol[::-1,:]

###########Hamiltoniano
def H(t,x,lam,U):
    u=lambda t: U
    f=SIR2p(x,t,u)
    return f[:4].dot(lam)-x[2]-x[3]





lam1=spline(t,lam[:,0],s=0)
lam2=spline(t,lam[:,1],s=0)
lam3=spline(t,lam[:,2],s=0)
lam4=spline(t,lam[:,3],s=0)

lam_func=lambda t: np.array([lam1(t),lam2(t),lam3(t),lam4(t)])

H_dim=lambda t: H(t,x_func(t),lam_func(t),u_func(t))
H_dim = np.vectorize(H_dim)

ax5.plot(t,lam2(t)*S2(t)-lam1(t)*S1(t))
ax5.legend((r'$\lambda_2(t)S_2(t)-\lambda_1(t)S_1(t)$',))
ax6.plot(t,H_dim(t))
ax6.legend((r'$H(t,x(t),\lambda(t))$',))

ax7.plot(t,J_val)
ax7.legend((r'$\int_0^T(I_1+I_2)dt$',))

ax8.plot(t,lam)#infeccionsos
ax8.legend((r'$\lambda_1$',r'$\lambda_2$',r'$\lambda_3$',r'$\lambda_4$'))


print("--- %s seconds ---" % (time.time() - start_time))