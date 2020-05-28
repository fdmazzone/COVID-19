#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sun May 10 07:55:03 2020

@author: fernando
"""

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
    Data=params[0]
    Y0,t_corte,alpha,R0a,R0b=x[:3],x[3],x[4],x[5],x[6]
    #Cambio escala tiempo
    s=np.arange(np.shape(Data)[0])*alpha
    s_corte=alpha*t_corte
    Sol = odeint(SIR,Y0 ,s, args=(s_corte,R0a,R0b))
    return max(np.abs(Data[:,1]-Sol[:,1]))
#max(np.abs(Data[:,1]-Sol[:,1]))




##################Ejemplo ajustando datos de Argentina ##############33
#Buscando datos
####
#Pais,Poblacion="Argentina",44e6
#### 
#Pais,Poblacion="Brazil",209.5e6
#######
#######
#Pais="Spain" 
#Poblacion=47007367
#######
#Pais="Italy"
#Poblacion=60541000 
#Pais,Poblacion="USA",325719178#recortar datos 34:
#Pais,Poblacion="Chile",19107216
Pais,Poblacion="Netherlands",17424978
Data=ExtraerDatos(Pais,Poblacion)
Data=Data[:,:]/Poblacion

##############################################
####       Minimizador Local     #############
##############################################

R0alim=.5,5.0
R0blim=.5,5.0
alphalim=1/30.0,1/1.0
param_lim=alphalim,R0alim,R0blim

########### Condicion Inicial 
Y0=Data[0,:3]
####### Rango Condicion Inicial
Y0_lim=(Y0[0],Y0[0]),(1.0/Poblacion,10.0/Poblacion), (0,0)

#### Rango tiempo corte
t=np.arange(np.shape(Data)[0])
t_corte_lim=((t[0],t[-1]),)


rangos=Y0_lim+t_corte_lim+param_lim
############  Candidato inicial ###############33
param0=np.array([20,1/5.5,3.0,1.3])
x0=np.concatenate([Y0,param0],0)


###########Minimizando

minimi_out= scipy.optimize.minimize(Error,x0,args=(Data[:,:],),method='TNC', bounds=rangos)
x_opt=minimi_out["x"]
error_opt=minimi_out["fun"]
#################Fin Minimizador Local






Y0_opt=x_opt[:3]
t_corte_opt=x_opt[3]
alpha_opt=x_opt[4]
R0a_opt=x_opt[5]
R0b_opt=x_opt[6]

########### Exponiendo datos

tt=np.arange(365)

s=alpha_opt*tt
s_corte_opt=alpha_opt*t_corte_opt

sol = odeint(SIR,Y0_opt ,s, args=(s_corte_opt,R0a_opt,R0b_opt))


S,I,R=sol[:,0],sol[:,1],sol[:,2]
plt.plot(tt,I*Poblacion,Data[:,1]*Poblacion,'+')
plt.yscale('log')

formato= "Y0        =     (%9.3E,%5.3f , %5.3f)\nt_corte   = %10.3f\n1/alpha   = %10.3f\nR0a       = %10.3f\nR0b       = %10.3f\nerror_out = %10.3e"   
Y0_for=Y0_opt*Poblacion


out=Y0_for[0],Y0_for[1],Y0_for[2], t_corte_opt, 1/alpha_opt, R0a_opt, R0b_opt, error_opt*Poblacion


print(formato% out)


