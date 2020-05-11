#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Ajuste de los datos de la pandemia a un modelo SIR
usando un minimizador global
Created on Thu May  7 08:13:53 2020
@author: Fernando Mazzone

"""


#Paquetes necesarios. 
import numpy as np
from scipy.integrate import odeint 
import matplotlib.pyplot as plt
import scipy.optimize

def funcionR0(t,t_corte,R0a,R0b,t_trans):
    if t<=t_corte-t_trans:
        R0=R0a
    elif t_corte-t_trans<t<=t_corte+t_trans:
        R0=(R0b-R0a)*(t-t_corte+t_trans)/(2*t_trans)+R0a
    else:
        R0=R0b
    return R0 




def SIR(Y,s,s_corte,R0a,R0b):
    #S,I,R=Y[0],Y[1],Y[2]
    t_trans=5
    dSds=-funcionR0(s,s_corte,R0a,R0b,t_trans)*Y[0]*Y[1]
    dIds=funcionR0(s,s_corte,R0a,R0b,t_trans)*Y[0]*Y[1]-Y[1]
    dRds=Y[1]
    return dSds,dIds,dRds

def Error(x,*params):
    Y0,Data=params
    t_corte,alpha,R0a,R0b=x
    #Cambio escala tiempo
    s=np.arange(np.shape(Data)[0])*alpha
    s_corte=alpha*t_corte
    Sol = odeint(SIR,Y0 ,s, args=(s_corte,R0a,R0b))
    return max(np.abs(Data[:,1]-Sol[:,1]))





##################Ejemplo ajustando datos de Argentina ##############33
#Buscando datos
####
#Pais="Argentina"    
#Poblacion=44e6
#Data=ExtraerDatos('Argentina',Poblacion)
#### 
#Pais="Brazil" 
#Poblacion=209.5e6
#######
#######
#Pais="Spain" 
#Poblacion=47007367
#######
#Pais="Italy"
#Poblacion=60541000 
Pais="USA"
Poblacion=325719178


Data=ExtraerDatos(Pais,Poblacion)
Data=Data[34:,:]/Poblacion #NOrmalizamos la poblacion total
############  tiempos
t=np.arange(np.shape(Data)[0])

##############################################
####       Minimizador Global    #############
##############################################
 

R0alim=2.5,5
R0blim=1.0,2.0
alphalim=1/3.0,1/15.0
t_corte_lim=(15.0,25.0)
#### Rango tiempo corte



rangos=t_corte_lim,alphalim,R0alim,R0blim

########### Condicion Inicial 
Y0=Data[0,:3]







opt=scipy.optimize.brute(Error,rangos,args=(Y0,Data),finish=None,full_output=True)
x_opt,error_opt=opt[0:2]





t_corte_opt,alpha_opt,R0a_opt,R0b_opt=x_opt


########### Exponiendo datos

tt=np.arange(365)

s=alpha_opt*tt
s_corte_opt=alpha_opt*t_corte_opt



sol =  odeint(SIR,Y0 ,s, args=(s_corte_opt,R0a_opt,R0b_opt))

S,I=sol[:,0],sol[:,1]
plt.plot(tt,I*Poblacion,t,Data[:,1]*Poblacion,'+')
plt.yscale('log')
plt.title(Pais)

formato= "t_corte   = %10.3f\n1/alpha   = %10.3f\nR0a       = %10.3f\nR0b       = %10.3f\nerror_out = %10.3e"   

out=t_corte_opt, 1/alpha_opt, R0a_opt, R0b_opt, error_opt*Poblacion


print(formato% out)


