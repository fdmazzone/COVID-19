#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Thu Jul  9 19:27:44 2020

@author: fernando
"""


def FitSEIR(Pais='Argentina',Provincia=None,dpto=None,Metodo="dual_annealing"):
    """
    ##########################################################################
    Ajuste de los datos de la pandemia del COVID-19 a un modelo SEIR usando un
    algorítmo para hallar mínimos globales.
    ##########################################################################
    Parametros:
             
            Pais: string 
                País que se quiere analizar. Previamente debe llenarse el archivo 
                Data/Countries/countries.csv con un rango donde se quiere se busqué
                los parámetros óptimos. El archivo provisto contiene datos de 
                algunos países
            
            Provincia: string
                      Solo posible si Pais='Argentina'.  Provincia Argetina.
                      base de rangos Data/Countries/DataFitProv.csv.
                      
            dpto: string
                    departamento que corresponda a la provincia elegida. 
                    Base de fiteos Data/dptos/DataFitDptos.csv
                
            Metodo: string
                    Metodo de optimización utilizado. La función ajusta un
                    modelo SEIR a los datos descargados. Valor por defecto 
                    "dual_annealing". Valores posibles "dual_annealing""shgo", 
                    "brute" 
            
     retorna
         gráfico donde se representan cantidad casos confirmados y sus 
            ajustes por el modelo SEIR
                    
    
  
    
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
    
    Creado Jueves 10-07-2020 09:58
    @author: Fernando Mazzone
    """

    ############  Ler datos de datos fiteos####################################
    if Provincia==None:
        Poblacion,st,R0_lim,t_corte_lim=load_fit_data_world(Pais)
       ########### Leer datos país ############################################
        DataC,DataR,DataM=readData(Pais)
        Ia=DataC[DataC>0].to_numpy()
        Id=DataC[DataC>0].diff().to_numpy()
        DataC[DataC>0].diff().to_numpy()
        M_data=DataM[DataC>0].to_numpy()
        R_data=DataR[DataC>0].to_numpy()
        tg=pd.to_datetime(DataC[DataC>0].index).to_numpy()
        Ia=Ia[st:]/Poblacion #NOrmalizamos la poblacion total}
        Id=Id[st:]
        M_data=M_data[st:]/Poblacion
        R_data=R_data[st:]/Poblacion
        tg=tg[st:]
        
        #############   tiempo en días desde inicio
        t=np.arange(len(tg))

    else:
        if not dpto==None:
            Poblacion,st,R0_lim,t_corte_lim=load_fit_data_dpto(Provincia,dpto)
            Data=readDataArg_dpto(Provincia, dpto)
        else:
            Poblacion,st,R0_lim,t_corte_lim=load_fit_data(Provincia)
            Data=readDataArg(Provincia)
        
        Ia=Data.CasosAcum.to_numpy()
        Id=Data.CasosDia.to_numpy()
        Ia=Ia[st:]/Poblacion #NOrmalizamos la poblacion total}
        Id=Id[st:]
        tg=pd.to_datetime(Data.index).to_numpy()
        tg=tg[st:]
        
        t=(tg-tg[0])/24.0/3600.0/1.0e9/np.timedelta64(1,'ns')
                   
    #### Rangos parametros fiteos
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

    if Provincia==None: 
        ax.set_title(unicode(Pais,"utf-8"),fontsize=26)
    elif not dpto==None:
        ax.set_title(unicode(dpto,"utf-8"),fontsize=26)
    else:
        ax.set_title(unicode(Provincia,"utf-8"),fontsize=26)

    ax.legend(('I Modelo','I datos'),shadow=True, loc=(.0, .8),\
              handlelength=1.5, fontsize=12)
    
    
    ############### Infectados diarios ######################################
       
    
    Id_mod=k*Poblacion*E
    ax.plot(t_tics,Id_mod,tg,Id,'o')
    ax.legend(('Modelo','Confirmados acumulados','Modelo', 'Confirmados diarios'),\
              shadow=True, loc=(.05, .82), handlelength=1.5, fontsize=12)
    
    ###############Datos a la derecha de la gráfica

    I_max=max(I)*Poblacion
    if len(t_corte_opt)>0:
        S0=S[int(t_corte_opt[-1])]
    else:
        S0=S[0]
    
    ##### Computamos relacion final
    f=lambda S_inf: np.log(S0/S_inf)-R0_opt[-1]*(1-S_inf)
    I_acum_inf=(1-scipy.optimize.fsolve(f,.000001))*Poblacion
    
    
    
    formato=""
    for j in t_corte_opt:
        formato+="%10.2f , "
    fig.text(0.7,0.5,r"$t_{corte}=$"+formato%tuple(t_corte_opt),fontsize=14)
    

    
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
    """
    Función tipo Heaveside pero la discontinuidad unida por una resta entre 
    [-epsilon,epsilon] 
    """
    out=np.zeros_like(t)
    I=(t>-epsilon)*(t<=epsilon)
    out[I]=t[I]/(2.0*epsilon)+.5
    I=t>epsilon
    out[I]=np.ones_like(t[I])
    return out

##############Funcion R0 escalera suavizada ###################################
def funcionR0(t,t_corte,R0):
    """
    Función R0(t) tipo escalera (pero continua)
    parametros:
        t: np array 1-dimensional
        t_corte: array de 2-tuples
                 zona donde se ajustan los cambios de R0
        R0: array de 2-tuples
           zona donde se ajustan los R0
    retorna
        np array R0(t)
    """
    S=R0[0]
    S+=sum((R0[j+1]-R0[j])*He(t-t_corte[j],epsilon) for j in range(len(t_corte)))
    return S

####  Mdelo SIR con funcion suavizada #########################################
def SEIR(Y,s,s_corte,R0):
    """
    Ecuaciones diferenciales del modelo SEIR
    
    Parametros:
               Y: 4-dimensional np.array containig SEIR
               s: time float64
               s_corte: np array de float64 (momentos de corte)
               R0: np array de float64 (valores de R0)
    retorna
        4-dimensional np.array S',E'I',R'.
    """
    dSds=-funcionR0(s,s_corte,R0)*Y[0]*Y[2]
    dEds=funcionR0(s,s_corte,R0)*Y[0]*Y[2]-k_ast*Y[1]
    dIds=k_ast*Y[1]-Y[2]
    dRds=Y[2]
    return dSds,dEds,dIds,dRds

#############   Funcion costo a minimizar ####################################
def Error(x,*params):
    """
    Calcula el error de un modelos SEIR respecto a datos 
    Parametros
              x: (2*n-1)-dimensional np.array, las primeras n componentes
                 son valores de R0 y las n-1 restantes son valores donde cambia
                 el R0
             params: 3-tuple, Primera componente un np.array 4d de condiciones
                     iniciales, segunda componente un np.array de datos de 
                     casos confirmados acumulados, tercera componente  np.array 
                     de tiempos
    retorna
         float64. Suma de cuadrados de los residuos respecto a los datos y el 
         modelo SEIR con los parámetros dados por x.
    
    """
    Y0,Ia,t=params
    n=(len(x)+1)/2
    t_corte,R0=x[:n-1],x[n-1:]
   #Cambio escala tiempo
    s=t*alpha
    s_corte=alpha*t_corte
    Sol = odeint(SEIR,Y0 ,s, args=(s_corte,R0))
    return sum(((np.abs(Ia-Sol[:,2]-Sol[:,3]-Sol[:,1])))**2)



##############################################################################
###################   Datos Epidemia  ########################################

########################### Provincias #######################################
def readDataArg(Provincia):
    """
    Lee datos de la base descargada del ministerio de salud de la República 
    Argentina.
    
    Parametros:
            Provincia: string, provincia Argentina.
    retorna:
           Pandas DataFrame. index: tiempos (datetime64[ns]), columna1: Casos 
           Acumulados (int64),  columna2: Casos Diarios(int64).
    """
    Data=pd.read_csv('Data/Epidemic/Covid19Casos.csv')   
    I1=Data.residencia_provincia_nombre==Provincia   
    I2=Data.clasificacion_resumen=="Confirmado" 
    DataProv=Data[I1 & I2] 
    CasosDia=DataProv.fecha_apertura.value_counts()
    CasosDia.index = pd.to_datetime(CasosDia.index)
    CasosDia=CasosDia.sort_index().rename('CasosDia')
    CasosAcum=CasosDia.cumsum().rename('CasosAcum')
    Data=pd.concat([CasosAcum,CasosDia], axis=1)
    return Data

#################### Departamentos ###########################################
def readDataArg_dpto(Provincia, dpto_nam):
    """
    Lee datos de la base descargada del ministerio de salud de la República 
    Argentina.
    
    Parametros:
            Provincia: string, provincia Argentina.
            dpto_nam: string, departamento perteneciente a Provincia
    retorna:
           Pandas DataFrame. index: tiempos (datetime64[ns]), columna1: Casos 
           Acumulados (int64),  columna2: Casos Diarios(int64).
    """
    Data=pd.read_csv('Data/Epidemic/Covid19Casos.csv')   
    I1=Data.residencia_provincia_nombre==Provincia
    I2=Data.residencia_departamento_nombre==dpto_nam
    I3=Data.clasificacion_resumen=="Confirmado" 
    DataProv=Data[I1 & I2 & I3] 
    CasosDia=DataProv.fecha_apertura.value_counts()
    CasosDia.index = pd.to_datetime(CasosDia.index)
    CasosDia=CasosDia.sort_index().rename('CasosDia')
    CasosAcum=CasosDia.cumsum().rename('CasosAcum')
    Data=pd.concat([CasosAcum,CasosDia], axis=1)
    return Data

######################  Paises ################################################
def readData(Pais):
    """
    Lee datos de la base descargada de 'https://data.humdata.org/'
    
    Parametros:
            Pais: string, nombre país en inglés
    retorna:
           3-tuple con DataC, DataM, DataR. Pandas DataSeries. index: tiempos 
           (datetime64[ns]), valores Casos Acumulados (int64).
    """
    DataC=pd.read_csv('Data/Epidemic/DataConfirmados.csv')
    DataM=pd.read_csv('Data/Epidemic/DataMuertos.csv')
    DataR=pd.read_csv('Data/Epidemic/DataRecuperados.csv')
    
    if not Pais=="Tierra":
        DataC=DataC[(DataC[['Country/Region']]==Pais)['Country/Region']]
        DataM=DataM[(DataM[['Country/Region']]==Pais)['Country/Region']]
        DataR=DataR[(DataR[['Country/Region']]==Pais)['Country/Region']]
        
    col=DataC.columns[4:]
    DataC=DataC.loc[:,col].sum()
    DataC.index=pd.to_datetime(DataC.index)
    
    
    DataM=pd.read_csv('Data/Epidemic/DataMuertos.csv')
    DataM=DataM[(DataM[['Country/Region']]==Pais)['Country/Region']]
    col=DataM.columns[4:]
    DataM=DataM.loc[:,col].sum()
    DataM.index=pd.to_datetime(DataM.index)
   
    
    DataR=pd.read_csv('Data/Epidemic/DataRecuperados.csv')
    DataR=DataR[(DataR[['Country/Region']]==Pais)['Country/Region']]
    col=DataR.columns[4:]
    DataR=DataR.loc[:,col].sum()
    DataR.index=pd.to_datetime(DataR.index)
    
    return DataC, DataM, DataR

##########################################################################
##################   Cargar rangos de ajuste, poblacion ##################
##########################################################################
####################   Paises ###############################################
def load_fit_data_world(Pais):
    """
    Carga los parámetros para usar en el ajuste del archivo 
    Data/Countries/countries.csv
    
    Parametros
              Pais: string, nombre del pais en ingles.
    Retorna:
            Poblacion: #habitantes, float 64
            st: int, los datos hasta st son descartados
            R0_lim: tuple de 2-tuples de float64. Rangos de R0 para ajustar
            t_corte_lim: tuple de 2-tuples de float64. Rangos de tiempos de 
                          corte para ajustar
    """
    DataFitWorld=pd.read_csv('Data/Countries/countries.csv')
    I=DataFitWorld.Pais==Pais
    DataFit=DataFitWorld[I]
    i0=DataFit.Poblacion.index[0]
    Poblacion=DataFit.Poblacion.loc[i0]
    st=DataFit.st.loc[i0]
    R0_min=DataFit.R0_min.loc[i0+1:]
    R0_max=DataFit.R0_max.loc[i0+1:]
    Indice=DataFit.index[1:]
    R0_lim=[(R0_min[i],R0_max[i]) for i in Indice]
    tc_min=DataFit.tc_min.loc[i0+2:]
    tc_max=DataFit.tc_max.loc[i0+2:]
    t_corte_lim=[(tc_min[i],tc_max[i]) for i in Indice[1:]]    
    return Poblacion,int(st),R0_lim,t_corte_lim    


###################  Provincias ##########################################
def load_fit_data(Provincia):
    """
    Carga los parámetros para usar en el ajuste del archivo 
    Data/Provincias/DataFitProv.csv
    
    Parametros
              Provincia: string, nombre de la provincia Argentina.
    Retorna:
            Poblacion: #habitantes, float 64
            st: int, los datos hasta st son descartados
            R0_lim: tuple de 2-tuples de float64. Rangos de R0 para ajustar
            t_corte_lim: tuple de 2-tuples de float64. Rangos de tiempos de 
                          corte para ajustar
    """
    DataFitArg=pd.read_csv('Data/Provincias/DataFitProv.csv')
    I=DataFitArg.Provincia==Provincia
    DataFitProv=DataFitArg[I]
    i0=DataFitProv.Poblacion.index[0]
    Poblacion=DataFitProv.Poblacion.loc[i0]
    st=DataFitProv.st.loc[i0]
    R0_min=DataFitProv.R0_min.loc[i0+1:]
    R0_max=DataFitProv.R0_max.loc[i0+1:]
    Indice=DataFitProv.index[1:]
    R0_lim=[(R0_min[i],R0_max[i]) for i in Indice]
    tc_min=DataFitProv.tc_min.loc[i0+2:]
    tc_max=DataFitProv.tc_max.loc[i0+2:]
    t_corte_lim=[(tc_min[i],tc_max[i]) for i in Indice[1:]]    
    return Poblacion,int(st),R0_lim,t_corte_lim

########################  Departamentos ###################################

def load_fit_data_dpto(Provincia,dpto_nam):
    """
    Carga los parámetros para usar en el ajuste desde los archivos 
    Data/Poblacion/poblacion_dpto.csv  y Data/dptos/DataFitDptos.csv'
    
    Parametros
              Provincia: string, nombre de la provincia Argentina.
              dpto_nam string, nombre del departamento.
    Retorna:
            Poblacion: #habitantes, float 64
            st: int, los datos hasta st son descartados
            R0_lim: tuple de 2-tuples de float64. Rangos de R0 para ajustar
            t_corte_lim: tuple de 2-tuples de float64. Rangos de tiempos de 
                          corte para ajustar
    """
    Data_dpto=pd.read_csv('Data/Poblacion/poblacion_dpto.csv')
    I=Data_dpto.provincia_name==Provincia
    I1=Data_dpto.nam==dpto_nam
    Data_dpto=Data_dpto[I & I1].personas
    Poblacion=float(Data_dpto[Data_dpto.index[0]])
    DataFitArg=pd.read_csv('Data/dptos/DataFitDptos.csv')
    I=DataFitArg.Provincia==Provincia
    I1=DataFitArg.nam==dpto_nam
    DataFitProv=DataFitArg[I & I1]
    i0=DataFitProv.index[0]
    st=DataFitProv.st.loc[i0]
    R0_min=DataFitProv.R0_min.loc[i0:]
    R0_max=DataFitProv.R0_max.loc[i0:]
    R0_lim=[(R0_min[i],R0_max[i]) for i in DataFitProv.index]
    tc_min=DataFitProv.tc_min.loc[i0+1:]
    tc_max=DataFitProv.tc_max.loc[i0+1:]
    t_corte_lim=[(tc_min[i],tc_max[i]) for i in DataFitProv.index[1:]]    
    return Poblacion,int(st),R0_lim,t_corte_lim





##########################################################################
################  Descargar Datos ########################################
##########################################################################


def downloadARG():
    """
    Descarga los datos de la epidemia del COVID-19 de
    https://sisa.msal.gov.ar/datos/descargas/covid-19/files/Covid19Casos.csv' 
    y los guarda en Data/Epidemic/Covid19Casos.csv
    
    Parametros: None
    
    Retorna:
         Data/Epidemic/Covid19Casos.csv
    """
    
    url=u'https://sisa.msal.gov.ar/datos/descargas/covid-19/files/Covid19Casos.csv'  
    with open('Data/Epidemic/Covid19Casos.csv', 'wb') as f:
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
    f= open('Data/Epidemic/Covid19Casos.csv', 'rb')
    content= unicode(f.read(), 'utf-16')
    f.close()
    f= open('Data/Epidemic/Covid19Casos.csv', 'wb')
    f.write(content.encode('utf-8'))
    f.close()

def downloadWorld():
    """
    Descarga los datos de la epidemia del COVID-19 desde 
    https://data.humdata.org y los guarda en 
    Data/Epidemic/DataConfirmados.csv 
    Data/Epidemic/DataMuertos.csv 
    Data/Epidemic/DataRecuperados.csv
    
    Parametros: None
    
    Retorna:
            Data/Epidemic/DataConfirmados.csv 
            Data/Epidemic/DataMuertos.csv 
            Data/Epidemic/DataRecuperados.csv 
    """
    
    
    urlb='https://data.humdata.org/hxlproxy/api/data-preview.csv?url=https%3A%2F%2Fraw.githubusercontent.com%2FCSSEGISandData%2FCOVID-19%2Fmaster%2Fcsse_covid_19_data%2Fcsse_covid_19_time_series%2F'
    url1 = 'time_series_covid19_confirmed_global.csv&filename=time_series_covid19_confirmed_global.csv'
    url2 = 'time_series_covid19_deaths_global.csv&filename=time_series_covid19_deaths_global.csv'
    url3 = 'time_series_covid19_recovered_global.csv&filename=time_series_covid19_recovered_global.csv'
    
    
    myfile = requests.get(urlb+url1)
    open('Data/Epidemic/DataConfirmados.csv', 'wb').write(myfile.content)
    
    myfile = requests.get(urlb+url2)
    open('Data/Epidemic/DataMuertos.csv', 'wb').write(myfile.content)
    
    myfile = requests.get(urlb+url3)
    open('Data/Epidemic/DataRecuperados.csv', 'wb').write(myfile.content)



###########################   Librerias ##################################### 
import numpy as np
from scipy.integrate import odeint 
import matplotlib.pyplot as plt
import scipy.optimize
import pandas as pd
from datetime import date
import requests
import sys


###################  Variables Globales ######################################
t_inf=3.0 
t_exp=5.0
alpha=1.0/t_inf
k=1.0/t_exp
k_ast=k/alpha
epsilon=1.0

  