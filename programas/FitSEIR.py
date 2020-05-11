#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Ajuste de los datos de la pandemia a un modelo SIER
Created on Thu May  7 08:13:53 2020
@author: Fernando Mazzone

"""

#Paquetes necesarios. 
import numpy as np
from scipy.integrate import odeint 
import matplotlib.pyplot as plt
import scipy.optimize

def SEIR(Y,t,R0):
    k_ast=1.0
    #R0,k_ast=params
    #S,I,E=Y
    dSds=-R0*Y[0]*Y[2]
    dIds=k_ast*Y[1]-Y[2]
    dEds=R0*Y[0]*Y[2]-k_ast*Y[1]
    return dSds,dIds,dEds


def Error(x,*params):
    Data=params[0]
    Y0,alpha,R0=x[:2],x[2],x[3]
    #Cambio escala tiempo
    s=np.arange(np.shape(Data)[0])*alpha  
    Sol = odeint(SIR,Y0 ,s, args=(R0,))
    return sum(np.abs(Data[:,1]-Sol[:,1]))
#max(np.abs(Data[:,1]-Sol[:,1]))




##################Ejemplo ajustando datos de Argentina ##############33
#Buscando datos
Poblacion=44e6
Data=ExtraerDatos('Argentina',Poblacion)
Data=Data/Poblacion #NOrmalizamos la poblacion total


#### Estableciendo los rangos de búsqueda de parámetros y
##condiciones iniciales     ##############################3
R0lim=.5,5.0
alphalim=1/30.0,1/5.0
param_lim=alphalim,R0lim
Y0=np.zeros(3)
Y0[:2]=Data[0,:2]

Y0_lim=(.9*Y0[0],Y0[0]),(0.1*Y0[1],2*Y0[1]), (0,.00001)
rangos=Y0_lim+param_lim
############  Candidato inicial ###############33
param0=np.array([1/10.0,3.0])#np.array([.5*sum(i) for i in rangos[3:]])
x0=np.concatenate([Y0,param0],0)
###########Minimizando




minimi_out= scipy.optimize.minimize(Error,x0,args=(Data[:18,:],),method='L-BFGS-B', bounds=rangos)
x_opt=minimi_out["x"]
error_opt=minimi_out["fun"]

Y0_opt=x_opt[:3]
alpha_opt=x_opt[3]
R0_opt=x_opt[4]

########### Exponiendo datos


k=len(Data[:,0])
t=np.arange(k)
s=alpha_opt*t
sol = odeint(SIR,Y0_opt ,s, args=(R0_opt,))

S,I=sol[:,0],sol[:,1]
plt.plot(t,I*Poblacion,t,Data[:,1]*Poblacion,'+')
plt.yscale('log')
print('Y0='+str(Y0_opt*Poblacion)+'\n1/alpha='+str(1/alpha_opt)+'\nR_0='+str(R0_opt)+'\n'+'Error'+str(error_opt))
