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
plt.rc('text', usetex=True)



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
"""
Pais,Poblacion="Argentina",44e6
R0alim=1.8,3.0
R0blim=1.0,1.5
alphalim=1/15.0,1/3.0
t_corte_lim=(15.0,20.0)
"""
#### 
"""
Pais,Poblacion="Brazil",209.5e6
R0alim=1.8,3.0
R0blim=1.0,1.5
alphalim=1/15.0,1/3.0
t_corte_lim=(15.0,30.0)
"""
#######
#######
#Pais="Spain" 
#Poblacion=47007367
#######
#Pais,Poblacion="Italy",60541000 
#Pais,Poblacion="USA",325719178#empezar de 34
Pais,Poblacion="Chile",19107216
R0alim=2.0,3.0
R0blim=1.0,1.5
alphalim=1/15.0,1/3.0
t_corte_lim=(18,25)


#Pais,Poblacion="Netherlands",17424978
#
#
############  tiempos


##############################################
####       Minimizador Global    #############
##############################################
 
Data=ExtraerDatos(Pais,Poblacion)
Data=Data[:53,:]/Poblacion #NOrmalizamos la poblacion total
t=np.arange(np.shape(Data)[0])

#### Rango tiempo corte



rangos=t_corte_lim,alphalim,R0alim,R0blim

########### Condicion Inicial 
Y0=Data[0,:3]



opt=scipy.optimize.dual_annealing(Error,rangos,args=(Y0,Data))
x_opt,error_opt=opt["x"],opt["fun"]

"""
opt=scipy.optimize.shgo(Error,rangos,args=(Y0,Data))
x_opt,error_opt=opt["x"],opt["fun"]
"""
"""
opt=scipy.optimize.brute(Error,rangos,args=(Y0,Data),finish=None,full_output=True)
x_opt,error_opt=opt[0:2]

"""


t_corte_opt,alpha_opt,R0a_opt,R0b_opt=x_opt


########### Exponiendo datos

tt=np.arange(365)

s=alpha_opt*tt
s_corte_opt=alpha_opt*t_corte_opt



sol =  odeint(SIR,Y0 ,s, args=(s_corte_opt,R0a_opt,R0b_opt))

S,I,R=sol[:,0],sol[:,1],sol[:,2]
plt.plot(tt,I*Poblacion,t,Data[:,1]*Poblacion,'o')
plt.yscale('log')
plt.title(Pais,fontsize=26)
plt.legend(('Modelo','Data'),shadow=True, loc=(.8, .8), handlelength=1.5, fontsize=16)
formato= "t_corte   = %10.3f\n1/alpha   = %10.3f\nR0a       = %10.3f\nR0b       = %10.3f\nerror_out = %10.3e"   

t_med=(tt[0]+tt[-1])/2
I_max=max(I)*Poblacion
I_med=I_max/300


alpha_opt_inv=1/alpha_opt

S0=S[int(t_corte_opt)]
f=lambda S_inf: np.log(S0/S_inf)-R0b_opt*(1-S_inf)
I_acum_inf=(1-scipy.optimize.fsolve(f,.000001))*Poblacion


plt.text(t_med,I_med,r"$\mathcal{R}_0^1=$"+"%10.2f"%R0a_opt,fontsize=16)
plt.text(t_med,I_med/5,r"$\mathcal{R}_0^2=$"+"%10.2f"%R0b_opt,fontsize=16)
plt.text(t_med,I_med/20,r"$\alpha^{-1}=$"+"%10.3f"%alpha_opt_inv,fontsize=16)
plt.text(t_med,I_med/100,r"$I_{max}=$"+"%10.2e"%I_max,fontsize=16)
plt.text(t_med,I_med/500,"Total Infectados="+"%10.4e"%I_acum_inf,fontsize=16)

out=t_corte_opt, 1/alpha_opt, R0a_opt, R0b_opt, error_opt*Poblacion
formato= "t_corte   = %10.3f\n1/alpha   = %10.3f\nR0a       = %10.3f\nR0b       = %10.3f\nerror_out = %10.3e"   


print(formato% out)


