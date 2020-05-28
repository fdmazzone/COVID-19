#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sat May 23 08:52:07 2020

@author: fernando
"""

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


############ Funciones Principales ###########################################
############# Función Heaviside suave ########################################
def He(t,epsilon):
    out=np.zeros_like(t)
    I=(t>-epsilon)*(t<=epsilon)
    out[I]=t[I]/(2.0*epsilon)+.5
    I=t>epsilon
    out[I]=np.ones_like(t[I])
    return out

##############Funcion R0 escalera suavizada ###################################
def funcionR0(t,t_corte,R0):
    epsilon=3.0
    S=R0[0]
    S+=sum((R0[j+1]-R0[j])*He(t-t_corte[j],epsilon) for j in range(len(t_corte)))
    return S

####  Mdelo SIR con funcion suavizada #########################################
def SIR(Y,s,s_corte,R0):
    #S,I,R=Y[0],Y[1],Y[2]
    dSds=-funcionR0(s,s_corte,R0)*Y[0]*Y[1]
    dIds=funcionR0(s,s_corte,R0)*Y[0]*Y[1]-Y[1]
    dRds=Y[1]
    return dSds,dIds,dRds

#############   Funcion costo a minimizar ####################################
def Error(x,*params):
    Y0,Data=params
    n=len(x)/2
    t_corte,alpha,R0=x[:n-1],x[n-1],x[n:]
   #Cambio escala tiempo
    s=np.arange(np.shape(Data)[0])*alpha
    s_corte=alpha*t_corte
    Sol = odeint(SIR,Y0 ,s, args=(s_corte,R0))
    return max(np.abs(Data[:,1]-Sol[:,1]))




################## Datos de paises  ##############
#### Se introducen limites basado en ajustes previos
####
"""
############# ARGENTINA  ##################
Pais,Poblacion="Argentina",44e6
t_corte_lim=((18.1,18.2),(76,80))
R0_lim=((2.47,2.48),(1.1,1.14),(1.1,2.0))
alphalim=((1/5.0,1/4.0),)
"""
#### 
"""
############# BRASIL #####################
Pais,Poblacion="Brazil",209.5e6
t_corte_lim=((28.1,29),(45,50))
R0_lim=((2.9,3.0),(1.3,1.4),(1.1,2.0))
alphalim=((1/6.5,1/5.5),)
"""
#######
#######
#Pais="Spain" 
#Poblacion=47007367
#######
#Pais,Poblacion="Italy",60541000 
#Pais,Poblacion="USA",325719178#empezar de 34


################ CHILE ####################
Pais,Poblacion="Chile",19107216
t_corte_lim=((19.66,22.0),(53.0,54.0))
R0_lim=((2.58,2.6),(1.03,1.05),(1.2,1.3))
alphalim=((1/3.9,1/3.7),)

#Pais,Poblacion="Netherlands",17424978
#
#
############  Ler datos #####################################################
Data=ExtraerDatos(Pais,Poblacion)
Data=Data[:,:]/Poblacion #NOrmalizamos la poblacion total}
t=np.arange(np.shape(Data)[0])


#### Rangos

rangos=t_corte_lim+alphalim+R0_lim

########### Condicion Inicial 

Y0=Data[0,:3]

################Elegir elmétodo deabajo  


"""
##############################################################################
####       Minimizadores Globales    ########################################
############## dual anneling: ##############################################
Xiang Y, Sun DY, Fan W, Gong XG. Generalized Simulated 
Annealing Algorithm and Its Application to the Thomson Model. 
Physics Letters A, 233, 216-220 (1997).
stochastic approach derived from [3] combines the generalization of CSA 
(Classical Simulated Annealing) and FSA (Fast Simulated Annealing) 
coupled to a strategy for applying a local search on accepted locations
Mas o menos rápido y bueno el ajuste. Produce diferentes resultados con difere-
tes corridas
############# shgo  ##########################################################
Sobol, IM (1967) “The distribution of points in a cube and the approximate 
evaluation of integrals”, USSR Comput. Math. Math. Phys. 7, 86-112. 
Global optimization using simplicial homology global optimisation [1]. 
Appropriate for solving general purpose NLP and blackbox optimisation problems
 to global optimality (low dimensional problems).
Más rápido menos bueno el ajuste
################ brute #######################################################
Minimize a function over a given range by brute force.
Uses the “brute force” method, i.e. computes the function’s value at each 
point of a multidimensional grid of points, to find the global minimum of 
the function.
Muy lento y muy preciso
#############  Minimize ######################################################
Solo minimos locales 
"""





opt=scipy.optimize.dual_annealing(Error,rangos,args=(Y0,Data))
x_opt,error_opt=opt["x"],opt["fun"]

"""
minimi_out= scipy.optimize.minimize(Error,x0,args=(Data[:,:],),method='TNC', bounds=rangos)
x_opt=minimi_out["x"]
error_opt=minimi_out["fun"]
"""
"""
opt=scipy.optimize.shgo(Error,rangos,args=(Y0,Data))
x_opt,error_opt=opt["x"],opt["fun"]
"""
"""
opt=scipy.optimize.brute(Error,rangos,args=(Y0,Data),finish=None,full_output=True)
x_opt,error_opt=opt[0:2]
"""





########### Exponiendo datos
n=len(x_opt)/2
t_corte_opt,alpha_opt,R0_opt=x_opt[:n-1],x_opt[n-1],x_opt[n:]

tt=np.arange(365)

s=alpha_opt*tt
s_corte_opt=alpha_opt*t_corte_opt

sol =  odeint(SIR,Y0 ,s, args=(s_corte_opt,R0_opt))

S,I,R=sol[:,0],sol[:,1],sol[:,2]

fig = plt.figure(figsize=(12,8))
ax = plt.axes([0.1, 0.1, 0.6, 0.8])

plot1=ax.plot(tt,I*Poblacion,t,Data[:,1]*Poblacion,'o')
ax.set(yscale='log')
ax.set(ylim=(1,Poblacion))
ax.set_title(Pais,fontsize=26)

ax.legend(('Modelo','Data'),shadow=True, loc=(.8, .8), handlelength=1.5, fontsize=16)

I_max=max(I)*Poblacion


alpha_opt_inv=1/alpha_opt

S0=S[int(t_corte_opt[-1])]


##### Computamos relacion final
f=lambda S_inf: np.log(S0/S_inf)-R0_opt[-1]*(1-S_inf)
I_acum_inf=(1-scipy.optimize.fsolve(f,.000001))*Poblacion

formato=""
for j in t_corte_opt:
    formato+="%10.2f , "
fig.text(0.75,0.5,r"$t_{corte}=$"+formato%tuple(t_corte_opt),fontsize=18)

formato=formato+"%10.2f"
fig.text(0.75,0.45,r"$\mathcal{R}_0=$"+formato%tuple(R0_opt),fontsize=18)
fig.text(0.75,0.4,r"$\frac{1}{\alpha}=$"+"%10.2f"%alpha_opt_inv+"d",fontsize=18)
fig.text(0.75,0.35,r"$I_{max}=$"+"%10.2e"%I_max+"h",fontsize=18)
fig.text(0.75,0.3,"$Total Inf.=$"+"%10.2e"%I_acum_inf+"h",fontsize=18)
error_out=error_opt*Poblacion
fig.text(0.75,0.25,r"$Error ajuste=$"+"%10.2e"%error_out+"h",fontsize=18)
