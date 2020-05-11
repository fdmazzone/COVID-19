#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Ajuste de los datos de la pandemia a un modelo SIR
Created on Thu May  7 08:13:53 2020
@author: Fernando Mazzone

"""


#Paquetes necesarios. 
import numpy as np
from scipy.integrate import odeint 
import matplotlib.pyplot as plt
import scipy.optimize


def SIR(Y,s,R0):
    #S,I,R=Y[0],Y[1],Y[2]
    dSds=-R0*Y[0]*Y[1]
    dIds=R0*Y[0]*Y[1]-Y[1]
    dRds=Y[1]
    return dSds,dIds,dRds


def Error(x,*params):
    Data=params[0]
    Y0,alpha,R0=x[:3],x[3],x[4]
    #Cambio escala tiempo
    s=np.arange(np.shape(Data)[0])*alpha  
    Sol = odeint(SIR,Y0 ,s, args=(R0,))
    return max(np.abs(Data[:,1]-Sol[:,1]))
#max(np.abs(Data[:,1]-Sol[:,1]))




##################Ejemplo ajustando datos de Argentina ##############33
#Buscando datos
####Argentina    
#Data=ExtraerDatos('Argentina',Poblacion)
#Poblacion=44e6
#### Brasil 
#Poblacion=209.5e6
#Data=ExtraerDatos('Brazil',Poblacion)
#######
#### China #####################
Poblacion=1403500365
Data=ExtraerDatos('China',Poblacion)


Data=Data/Poblacion #NOrmalizamos la poblacion total


#### Estableciendo los rangos de búsqueda de parámetros y
##condiciones iniciales     ##############################3
R0lim=.5,5.0
alphalim=1/30.0,1/1.0
param_lim=alphalim,R0lim
Y0=Data[0,:3]
Y0_lim=(.99*Y0[0],Y0[0]),(.9*Y0[1],1.1*Y0[1]), (.9*Y0[2],1.1*Y0[2])
rangos=Y0_lim+param_lim
############  Candidato inicial ###############33
param0=np.array([1/10.0,3])
x0=np.concatenate([Y0,param0],0)
###########Minimizando


"""
opt=scipy.optimize.brute(Error,rangos,args=(Data[:18,:],),finish=None,full_output=True)
x_opt,error_opt=opt[0:2]


"""
minimi_out= scipy.optimize.minimize(Error,x0,args=(Data[:15,:],),method='TNC', bounds=rangos)
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

formato= "Y0        =      (%10.3E,%5.3f , %5.3f)\n1/alpha   = %10.3f\nR0        = %10.3f\nerror_out = %10.3f"   
Y0_for=Y0_opt*Poblacion
out=Y0_for[0],Y0_for[1],Y0_opt[2], 1/alpha_opt, R0_opt, error_opt


print(formato% out)
