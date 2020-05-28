#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Thu May 14 17:03:51 2020

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
from scipy.integrate import odeint, simps
import matplotlib.pyplot as plt
import scipy.optimize
plt.rc('text', usetex=True)


H=lambda t:np.heaviside(t,1)
def funcionR0(t,t_corte,R0):
    S=sum(R0[j-1]*( H(t-t_corte[j-1])-H(t-t_corte[j])) for j in range(1,len(R0)))
    S=S+R0[-1]*H(t-t_corte[-1])#+R0[0]*H(t_corte[0]-t)
    return S

def SIR(Y,s,s_corte,R0):
    #S,I,R=Y[0],Y[1],Y[2]
    dSds=-funcionR0(s,s_corte,R0)*Y[0]*Y[1]
    dIds=funcionR0(s,s_corte,R0)*Y[0]*Y[1]-Y[1]
    dRds=Y[1]
    return dSds,dIds,dRds

def funcion_costo(R0,params):
    t_corte,Y0,t,R_max,R_min=params
    Sol = odeint(SIR,Y0 ,t, args=(t_corte,R0))
    #Int_R0=simps(funcionR0(t,t_corte,R0),t)
    Int_R0=simps((funcionR0(t,t_corte,R0)-R_min)**2/(R_max-R_min)**2,t)/t_corte[-1]
    #Int_I=simps(Sol[:,1],t)
    Int_I=max(Sol[:,1])*6.37504
    return Int_I-Int_R0

T=100
k=6
R_min=1.0
R_max=3
t_corte=np.linspace(0,T,k)[:-1]
rangos=[(R_min,R_max) for i in range(k-1)]
Y0=np.array([1.0,1e-4,0])
t=np.linspace(0,T,100*k)
R0=2*np.ones_like(t_corte)
params=t_corte,Y0,t,R_max,R_min
funcion_costo(R0,params)


"""
opt=scipy.optimize.brute(funcion_costo,rangos,args=(params,),finish=None,full_output=True)
R0_opt,f_costo=opt[0:2]
"""
"""
minimi_out= scipy.optimize.minimize(funcion_costo,R0,args=(params,),method='TNC', bounds=rangos)
R0_opt,f_costo=minimi_out["x"],minimi_out["fun"]
"""
"""
resultado=scipy.optimize.differential_evolution(funcion_costo,rangos,args=(params,))
R0_opt=resultado.x
f_costo=resultado.fun
"""
"""
resultado=scipy.optimize.dual_annealing(funcion_costo,rangos,args=(params,))
R0_opt=resultado.x
f_costo=resultado.fun
"""

resultado=scipy.optimize.shgo(funcion_costo,rangos,args=(params,))
R0_opt=resultado.x
f_costo=resultado.fun


print("R0_opt={0},\nCosto= {1:4.2f}".format(R0_opt,f_costo))

Sol = odeint(SIR,Y0 ,t, args=(t_corte,R0_opt))
Int_R0=simps(funcionR0(t,t_corte,R0_opt),t)
Int_I=simps(Sol[:,1],t)

fig = plt.figure()
ax = fig.add_subplot(2, 1,1 )
ax.plot(t,funcionR0(t,t_corte,R0_opt))
ax2 = fig.add_subplot(2, 1,2 )
ax2.plot(t,Sol[:,1])
ax2.set_yscale('log')
 




