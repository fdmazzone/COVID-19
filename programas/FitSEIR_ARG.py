#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon Jun 15 15:14:08 2020

@author: fernando
"""

#!/usr/bin/env python2
# -*- coding: utf-8 -*-


def FitSEIR_ARG(Provincia,dpto=None,Metodo="dual_annealing"):
    
    """
    ##########################################################################
    Ajuste de los datos de la pandemia del COVID-19 a un modelo SEIR usando un
    algorítmo para hallar mínimos globales.
    
    Uso de la función principal:
    
    >>AjusteSEIR(Pais)
    
    Pais=Pais elegido. 
    
    Debe ser "Argentina", "Chile", "Brazil", "Italy" o  "Spain". Se descargan 
    datos de contagios del resto de los países del mundo. Para agregar países
    editar el diccionario DatosPaises definido más abajo. Hay que agregar datos 
    de población total y rangos de búsqueda de los parámetros.
    
    La función ajusta un modelo SEIR a los datos descargados. Por defecto se 
    utiliza un minimizador global llamado dual_annealing. Los resultados se 
    presentan en un gráfico donde se representan cantidad casos confirmados y 
    diarios.   Se recomienda ejecutar antes DescargarData.py  que descarga los 
    últimos datos sobre la pandemia.
    
    Aternativamente
    
    >>AjusteSEIR(Pais,Metodo)
    
    Metodo puede ser: "dual_annealing" (dado por defecto), "shgo", "brute" 
    (muy lento)
  
    
    ###########################################################################
    ####       Minimizadores Globales.   ######################################
    
    Datos desde la docunmentacio oficial
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
    
    Creado Jueves 3-06-2020 08:13:53 2020
    @author: Fernando Mazzone
    """

    ############  Ler datos de datos fiteos####################################
    if not dpto==None:
        Poblacion,R0_lim,t_corte_lim=load_fit_data_dpto(Provincia,dpto)
        Ia,Id,tg=readDataArg_dpto(Provincia, dpto)
    else:
        Poblacion,R0_lim,t_corte_lim=load_fit_data(Provincia)
        Ia,Id,tg=readDataArg(Provincia)
    
    
    t=(tg-tg[0])/24.0/3600.0/1.0e9/np.timedelta64(1,'ns')
    Ia=Ia/Poblacion #NOrmalizamos la poblacion total}
       
    
    #### Rangos
    rangos=t_corte_lim+R0_lim
    
    ########### Condicion Inicial 
    Y0=[1.0,0.0,Ia[0],0.0]
    
   
    
    
    ################Elegir el método  
      
    if Metodo=='dual_annealing':
        opt=scipy.optimize.dual_annealing(Error,rangos,args=(Y0,Ia,t))
        x_opt,error_opt=opt["x"],opt["fun"]
    elif Metodo=='shgo':
        opt=scipy.optimize.shgo(Error,rangos,args=(Y0,Ia,t))
        x_opt,error_opt=opt["x"],opt["fun"]
    elif Metodo=='brute':
        opt=scipy.optimize.brute(Error,rangos,args=(Y0,Ia,t),finish=None,full_output=True)
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
    t_tics=pd.Series(pd.date_range(str(tg[0]), freq='D', periods=365))
    s=alpha*tt
    s_corte_opt=alpha*t_corte_opt
    sol =  odeint(SEIR,Y0 ,s, args=(s_corte_opt,R0_opt))
    S,E,I,R=sol[:,0],sol[:,1],sol[:,2],sol[:,3]
    

    ##########################################################################
    ################## Creacion graficas######################################
    ##########################################################################

    fig = plt.figure(figsize=(14,10))
    
    ###  Grafica de infectados acumulados###################################
    ax = plt.axes([0.1, 0.1, 0.5, 0.8])
    ax.plot(t_tics,(I+E+R)*Poblacion,tg,Ia*Poblacion,'o')
    ax.set(yscale='log')
    ax.set(ylim=(1,Poblacion))
    today = date.today()

    if not dpto==None:
        ax.set_title(unicode(dpto,"utf-8"),fontsize=26)
    else:
        ax.set_title(unicode(Provincia,"utf-8"),fontsize=26)

    ax.legend(('I Modelo','I datos'),shadow=True, loc=(.0, .8),\
              handlelength=1.5, fontsize=12)
    
    
    ############### Infectados diarios ######################################
       
    
    Id_mod=k*Poblacion*E
    ax.plot(t_tics,Id_mod,tg,Id,'o')
    ax.legend(('Modelo','Confirmados acumulados','Modelo', 'Confirmados diarios'),\
              shadow=True, loc=(.1, .7), handlelength=1.5, fontsize=12)
    
    ###############Datos a la derecha de la gráfica

    I_max=max(I)*Poblacion
    S0=S[int(t_corte_opt[-1])]
    
    
    ##### Computamos relacion final
    f=lambda S_inf: np.log(S0/S_inf)-R0_opt[-1]*(1-S_inf)
    I_acum_inf=(1-scipy.optimize.fsolve(f,.000001))*Poblacion
    
    
    
    formato=""
    for j in t_corte_opt:
        formato+="%10.2f , "
    fig.text(0.7,0.5,r"$t_{corte}=$"+formato%tuple(t_corte_opt),fontsize=14)
    
    t_inf=1/alpha
    t_exp=1/k
    
    formato=formato+"%10.2f"
    fig.text(0.7,.55,"Fecha: "+str(today),fontsize=14)
    fig.text(0.7,0.45,r"$\mathcal{R}_0=$"+formato%tuple(R0_opt),fontsize=14)
    fig.text(0.7,0.4,r"$t_{inf}=$"+"%10.2f"%t_inf+"d",fontsize=14)
    fig.text(0.7,0.35,r"$t_{exp}=$"+"%10.2f"%t_exp+"d",fontsize=14)
    fig.text(0.7,0.30,r"$I_{max}=$"+"%10.2e"%I_max+"h",fontsize=14)
    fig.text(0.7,0.25,"$Total Inf.=$"+"%10.2e"%I_acum_inf+"h",fontsize=14)
    error_out=np.sqrt(error_opt)*Poblacion
  
    fig.text(0.7,0.2,r"$Error ajuste=$"+"%10.2e"%error_out+"h",fontsize=14)


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
    Y0,Ia,t=params
    n=(len(x)+1)/2
    t_corte,R0=x[:n-1],x[n-1:]
   #Cambio escala tiempo
    s=t*alpha
    s_corte=alpha*t_corte
    Sol = odeint(SEIR,Y0 ,s, args=(s_corte,R0))
    return sum(((np.abs(Ia-Sol[:,2]-Sol[:,3]-Sol[:,1])))**2)


def readDataArg(Provincia):
    Data=pd.read_csv(fileData)   
    I1=Data.residencia_provincia_nombre==Provincia   
    I2=Data.clasificacion_resumen=="Confirmado" 
    DataProv=Data[I1 & I2] 
    CasosDia=DataProv.fecha_apertura.value_counts()
    CasosDia.index = pd.to_datetime(CasosDia.index)
    CasosDia=CasosDia.sort_index()
    CasosAcum=CasosDia.cumsum()
    I_acum=CasosAcum.to_numpy()
    I_diario=CasosDia.to_numpy()
    t_g=CasosDia.index.to_numpy()
    return I_acum,I_diario, t_g

def readDataArg_dpto(Provincia, dpto_nam):
    Data=pd.read_csv(fileData)   
    I1=Data.residencia_provincia_nombre==Provincia
    I2=Data.residencia_departamento_nombre==dpto_nam
    I3=Data.clasificacion_resumen=="Confirmado" 
    DataProv=Data[I1 & I2 & I3] 
    CasosDia=DataProv.fecha_apertura.value_counts()
    CasosDia.index = pd.to_datetime(CasosDia.index)
    CasosDia=CasosDia.sort_index()
    CasosAcum=CasosDia.cumsum()
    I_acum=CasosAcum.to_numpy()
    I_diario=CasosDia.to_numpy()
    t_g=CasosDia.index.to_numpy()
    return I_acum,I_diario, t_g

def download():
    with open(fileData, 'wb') as f:
        response = requests.get(url, stream=True)
        total = response.headers.get('content-length')

        if total is None:
            f.write(response.content)
        else:
            downloaded = 0
            total = int(total)
            for data in response.iter_content(chunk_size=max(int(total/1000), 1024*1024)):
                downloaded += len(data)
                f.write(data)
                done = int(50*downloaded/total)
                sys.stdout.write('\r[{}{}]'.format('█' * done, '.' * (50-done)))
                sys.stdout.flush()
    sys.stdout.write('\n')
    f= open(fileData, 'rb')
    content= unicode(f.read(), 'utf-16')
    f.close()
    f= open(fileData, 'wb')
    f.write(content.encode('utf-8'))
    f.close()
##########################################################################
##################   Cargar rangos de ajuste, poblacion ##################
##########################################################################

def load_fit_data(Provincia):
    DataFitArg=pd.read_csv(filepath)
    I=DataFitArg.Provincia==Provincia
    DataFitProv=DataFitArg[I]
    i0=DataFitProv.Poblacion.index[0]
    Poblacion=DataFitProv.Poblacion.loc[i0]
    R0_min=DataFitProv.R0_min.loc[i0+1:]
    R0_max=DataFitProv.R0_max.loc[i0+1:]
    Indice=DataFitProv.index[1:]
    R0_lim=[(R0_min[i],R0_max[i]) for i in Indice]
    tc_min=DataFitProv.tc_min.loc[i0+2:]
    tc_max=DataFitProv.tc_max.loc[i0+2:]
    t_corte_lim=[(tc_min[i],tc_max[i]) for i in Indice[1:]]    
    return Poblacion,R0_lim,t_corte_lim

def load_fit_data_dpto(Provincia,dpto_nam):
    Data_dpto=pd.read_csv(dir_working+'/Data/Poblacion/poblacion_dpto.csv')
    I=Data_dpto.provincia_name==Provincia
    I1=Data_dpto.nam==dpto_nam
    Data_dpto=Data_dpto[I & I1].personas
    Poblacion=float(Data_dpto[Data_dpto.index[0]])
    DataFitArg=pd.read_csv(dir_working+'/Data/dptos/DataFitDptos.csv')
    I=DataFitArg.Provincia==Provincia
    I1=DataFitArg.nam==dpto_nam
    DataFitProv=DataFitArg[I & I1]
    i0=DataFitProv.index[0]
    R0_min=DataFitProv.R0_min.loc[i0:]
    R0_max=DataFitProv.R0_max.loc[i0:]
    R0_lim=[(R0_min[i],R0_max[i]) for i in DataFitProv.index]
    tc_min=DataFitProv.tc_min.loc[i0+1:]
    tc_max=DataFitProv.tc_max.loc[i0+1:]
    t_corte_lim=[(tc_min[i],tc_max[i]) for i in DataFitProv.index[1:]]    
    return Poblacion,R0_lim,t_corte_lim




#Paquetes necesarios. 
import numpy as np
from scipy.integrate import odeint 
import matplotlib.pyplot as plt
import scipy.optimize
import pandas as pd
from datetime import date
import requests
import sys
import os



############## DIRECTORIO Y LINKS ##############################
################################################################
dir_working=unicode(os.getcwd(),'utf-8')
fileData=dir_working+u"/Data/Epidemic/Covid19Casos.csv"
url=u'https://sisa.msal.gov.ar/datos/descargas/covid-19/files/Covid19Casos.csv'  
filepath=dir_working+u'/Data/Provincias/DataFitProv.csv'
  
#def readDataARG():
#plt.rc('text', usetex=True)
#plt.rc('font', family='Arial')
#FitSEIR_ARG('Córdoba','shgo')
#################  ASIGNACION PARAMETROS GLOBALES#########################
##########################################################################

alpha=1/3.0 #1/Periodo infecciosidad  
k=1/5.0     #1/Periodo exposicion 
k_ast=k/alpha # adimensionalización
epsilon=1.0  #AMPLITUD DÍAS TANSICION R0