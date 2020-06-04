#!/usr/bin/env python2
# -*- coding: utf-8 -*-

"""
##############################################################################
Ajuste de los datos de la pandemia a un modelo SEIR usando un minimizador 
global.

Uso de la función principal:

>>AjusteSEIR(Pais)

Pais=Pais elegido. Debe ser "Argentina", "Chile", "Brazil", "Italy" o "Spain"

La función ajusta un modelo SEIR a los datos descargados. Por defecto se 
utiliza un minimizador global llamado dual_annealing. Los resultados se 
presentan en un gráfico donde se representan cantidad casos confirmados y 
diarios. 

Aternativamente

>>AjusteSEIR(Pais,Metodo)
Metodo puede ser: "dual_annealing" (dado por defecto), "shgo", "brute" (muy lento)

Se recomienda ejecutar antes DescargarData.py  que descarga los últimos datos 
sobre la pandemia.

Creado Jueves Mayo  7 08:13:53 2020
@author: Fernando Mazzone
##############################################################################
"""


#Paquetes necesarios. 
import numpy as np
from scipy.integrate import odeint 
import matplotlib.pyplot as plt
import scipy.optimize
import csv
plt.rc('text', usetex=True)



#### Datos de paises  ######################################
#### Se introducen limites basado en ajustes previos #######
#### Formato: Pais:[Poblacion,rango cortes,rangos R0]
########   Los datos dados fueron obtenidos experimentalemente

DatosPaises=\
    {"Argentina":[44e6, ((19.0,20.0),(78.0,79.0)),((3.5,4.5),(1.0,2.0),(1.0,2.0))],
      "Brazil":[209.5e6,((28.1,29),(45,50)),((3.,5.0),(1.0,3.0),(1.0,3.0))],
      "Spain": [47007367.0,((15,50),),((3.,5.0),(0.0,1.0))],#Empezar en 23
      "Italy": [60541000,((15,50),(50,100)),((3.,5.0),(0.0,1.0),(0.0,1.0))],
      "Chile": [19107216,\
                ((19.66,22.0),(53.0,54.0)),((2.58,2.6),(1.03,1.05),(1.2,1.3))],
      "USA":   [325719178,(),()]#empezar de 34
    }

    
#################  ASIGNACION PARAMETROS GLOBALES#########################
##########################################################################
alpha=1/3.0 #1/Periodo infecciosidad  
k=1/5.0     #1/Periodo exposicion 
k_ast=k/alpha # adimensionalización
epsilon=3.0  #AMPLITUD DÍAS TANSICION R0

def AjusteSEIR(Pais,Metodo="dual_annealing"):
        
    """
    #######################   Descripcion ###################################
    Esta funcion ajusta un modelo SEIR a datos de la pandemia del COVID-19.
    Pais:  pais o region del que se quieren qjustar los datos. Debe figurar
    en la base de paises DatosPaises
    
    
    
    ######    Metodos de minimizacion    ######################################
    ###########################################################################
    ####       Minimizadores Globales    ######################################
    ############## dual anneling: #############################################
    Xiang Y, Sun DY, Fan W, Gong XG. Generalized Simulated 
    Annealing Algorithm and Its Application to the Thomson Model. 
    Physics Letters A, 233, 216-220 (1997).
    stochastic approach derived from [3] combines the generalization of CSA 
    (Classical Simulated Annealing) and FSA (Fast Simulated Annealing) 
    coupled to a strategy for applying a local search on accepted locations
    Mas o menos rápido y bueno el ajuste. Produce diferentes resultados con 
    diferetes corridas
    ############# shgo  #######################################################
    Sobol, IM (1967) “The distribution of points in a cube and the approximate 
    evaluation of integrals”, USSR Comput. Math. Math. Phys. 7, 86-112. 
    Global optimization using simplicial homology global optimisation [1]. 
    Appropriate for solving general purpose NLP and blackbox optimisation 
    problems to global optimality (low dimensional problems).
    Más rápido menos bueno el ajuste
    ################ brute ####################################################
    Minimize a function over a given range by brute force.
    Uses the “brute force” method, i.e. computes the function’s value at each 
    point of a multidimensional grid of points, to find the global minimum of 
    the function.
    Muy lento y muy preciso
    """
     

    ############  Ler datos ##################################################
    Poblacion=DatosPaises[Pais][0]
    Data=ExtraerDatos(Pais,Poblacion)
    Data=Data[:,:]/Poblacion #NOrmalizamos la poblacion total}
    t=np.arange(np.shape(Data)[0])
    
    
    
    #### Rangos
    t_corte_lim=DatosPaises[Pais][1]
    R0_lim=DatosPaises[Pais][2]
    rangos=t_corte_lim+R0_lim
    
    ########### Condicion Inicial 
    Y0=[Data[0,0],0.0,Data[0,1],Data[0,2]]
    
    
    
    
    
    ################Elegir el método  
      
    if Metodo=='dual_annealing':
        opt=scipy.optimize.dual_annealing(Error,rangos,args=(Y0,Data))
        x_opt,error_opt=opt["x"],opt["fun"]
    elif Metodo=='shgo':
        opt=scipy.optimize.shgo(Error,rangos,args=(Y0,Data))
        x_opt,error_opt=opt["x"],opt["fun"]
    elif Metodo=='brute':
        opt=scipy.optimize.brute(Error,rangos,args=(Y0,Data),finish=None,full_output=True)
        x_opt,error_opt=opt[0:2]
    else:
        print("No existe el método"+Metodo )
        return
    
    
    
    
    
    ########### Exponiendo datos
    ### Extracción los resultados optimizacion
    n=(len(x_opt)+1)/2
    t_corte_opt=x_opt[:n-1]
    R0_opt=x_opt[n-1:]
    
    ###  Calculo curva teórica resultante
    tt=np.arange(365)
    s=alpha*tt
    s_corte_opt=alpha*t_corte_opt
    sol =  odeint(SEIR,Y0 ,s, args=(s_corte_opt,R0_opt))
    S,E,I,R=sol[:,0],sol[:,1],sol[:,2],sol[:,3]
    
    
    ##########################################################################
    ################## Creacion graficas######################################
    ##########################################################################
    
    fig = plt.figure(figsize=(12,8))
    
    ###  Grafica de infectados acumulados###################################
    ax = plt.axes([0.1, 0.1, 0.6, 0.8])
    ax.plot(tt,(I+E+R)*Poblacion,t,Data[:,4]*Poblacion,'o')
    ax.set(yscale='log')
    ax.set(ylim=(1,Poblacion))
    ax.set_title(Pais,fontsize=26)
    ax.legend(('I Modelo','I datos'),shadow=True, loc=(.8, .8),\
              handlelength=1.5, fontsize=16)
    
    
    ############### Infectados diarios ######################################
       
    I_d_data=(Data[1:,4]-Data[:-1,4])*Poblacion
    Id=k*Poblacion*E
    ax.plot(tt[:],Id,t[:-1],I_d_data,'o')
    ax.legend(('Modelo','Confirmados acumulados','Modelo', 'Confirmados diarios'),\
              shadow=True, loc=(.7, .7), handlelength=1.5, fontsize=16)
    
    ###############Datos a la derecha de la gráfica
    
    I_max=max(I)*Poblacion
    S0=S[int(t_corte_opt[-1])]
    
    
    ##### Computamos relacion final
    f=lambda S_inf: np.log(S0/S_inf)-R0_opt[-1]*(1-S_inf)
    I_acum_inf=(1-scipy.optimize.fsolve(f,.000001))*Poblacion
    
    
    
    formato=""
    for j in t_corte_opt:
        formato+="%10.2f , "
    fig.text(0.75,0.5,r"$t_{corte}=$"+formato%tuple(t_corte_opt),fontsize=18)
    
    t_inf=1/alpha
    t_exp=1/k
    
    formato=formato+"%10.2f"
    fig.text(0.75,0.45,r"$\mathcal{R}_0=$"+formato%tuple(R0_opt),fontsize=18)
    fig.text(0.75,0.4,r"$t_{inf}=$"+"%10.2f"%t_inf+"d",fontsize=18)
    fig.text(0.75,0.35,r"$t_{exp}=$"+"%10.2f"%t_exp+"d",fontsize=18)
    fig.text(0.75,0.30,r"$I_{max}=$"+"%10.2e"%I_max+"h",fontsize=18)
    fig.text(0.75,0.25,"$Total Inf.=$"+"%10.2e"%I_acum_inf+"h",fontsize=18)
    error_out=error_opt*Poblacion
    fig.text(0.75,0.2,r"$Error ajuste=$"+"%10.2e"%error_out+"h",fontsize=18)












############ Funciones Auxiliares ###########################################
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
    S=R0[0]
    S+=sum((R0[j+1]-R0[j])*He(t-t_corte[j],epsilon) for j in range(len(t_corte)))
    return S

####  Mdelo SIR con funcion suavizada #########################################
def SEIR(Y,s,s_corte,R0):
    #S,E,I,R=Y[0],Y[1],Y[2],Y[3]
    dSds=-funcionR0(s,s_corte,R0)*Y[0]*Y[2]
    dEds=funcionR0(s,s_corte,R0)*Y[0]*Y[2]-k_ast*Y[1]
    dIds=k_ast*Y[1]-Y[2]
    dRds=Y[2]
    return dSds,dEds,dIds,dRds

#############   Funcion costo a minimizar ####################################
def Error(x,*params):
    Y0,Data=params
    n=(len(x)+1)/2
    t_corte,R0=x[:n-1],x[n-1:]
   #Cambio escala tiempo
    s=np.arange(np.shape(Data)[0])*alpha
    s_corte=alpha*t_corte
    Sol = odeint(SEIR,Y0 ,s, args=(s_corte,R0))
    return max((np.abs(Data[:,4]-Sol[:,2]-Sol[:,3]-Sol[:,1])))

def ExtraerDatos(Pais,Poblacion):
    if Pais=='USA':
        I_data_acum=np.array([])
        I_data=np.array([])
        M_data=np.array([])
        R_data=np.array([])
        S_data=np.array([])

        with open('DataUSA.csv') as csvfile:
            reader = csv.reader(csvfile)
            next(reader)
            for row in reader:
                I_data_acum=np.append(I_data_acum,float(row[2]))
                M_data=np.append(M_data,float('0'+row[14]))
                R_data=np.append(R_data,float('0'+row[11]))
                
            I_data_acum=np.flip(I_data_acum)
            M_data=np.flip(M_data)
            R_data=np.flip(R_data)
    else:
        with open('DataConfirmados.csv') as csvfile:
            reader = csv.reader(csvfile)
            I_data_acum,M_data,R_data=0,0,0
            for row in reader:
                if Pais in row:
                    I_data_acum+=np.array([float(i) for i in row[5:]])
        with open('DataMuertos.csv') as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                if Pais in row:
                    M_data+=np.array([float(i) for i in row[5:]])
        with open('DataRecuperados.csv') as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                if Pais in row:
                    R_data+=np.array([float(i) for i in row[5:]])
        i0=min(len(I_data_acum),len(M_data),len(R_data))
        I0=range(i0)
        I_data_acum=I_data_acum[I0]
        R_data=R_data[I0]
        M_data=M_data[I0]


        #Extraemos datos desde el comienzo de la epidemia
    I_data=I_data_acum-(M_data+R_data)
    S_data=Poblacion-I_data_acum #S=Poblacion-Infectados Acumulados
    Ind=I_data_acum>0
    k=sum(Ind)
    #Data=[S,I,R,M,Iacum]
    Data=np.zeros([k,5])
    Data[:,0]=S_data[Ind]
    Data[:,1]=I_data[Ind]
    Data[:,2]=R_data[Ind]
    Data[:,3]=M_data[Ind]
    Data[:,4]=I_data_acum[Ind]

    return Data