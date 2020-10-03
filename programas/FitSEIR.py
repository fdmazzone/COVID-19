#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Thu Jul  9 19:27:44 2020

@author: fernando
"""


def FitSEIR(Pais='Argentina',Provincia=None,dpto=None,fecha=(), R0_lim=(),R0_fijo=(),t_lim=(),t_lim_fijo=(),Metodo='shgo'):
    """
    ##########################################################################
    Ajuste de los datos de la pandemia del COVID-19 a un modelo SEIR usando un
    algorítmo para hallar mínimos globales.
    ##########################################################################
    Parametros:
             
            Pais: string 
                País que se quiere analizar. Previamente debe llenarse el archivo 
                Data/Countries/countries.csv con  la población total del país
            
            Provincia: string
                      Solo posible si Pais='Argentina'.  
            
            dpto: string
                    departamento que corresponda a la provincia elegida. 
                    Base de fiteos Data/dptos/DataFitDptos.csv

            fecha: tuple de strings
                    fecha 2-tuple con fechas en formato 'AAAA-MM-DD', 
                    rango de tiempo del análisis
                    
            R0_fijo: tuple de float64
                    valores fijos (no ajustables) de R0, 
                    deben ser los primeros

            R0_lim: tuple de 2-tuples de float 64
                    rangos donde se buscarán los valores de R0 que son 
                    ajustables.

            t_fijo_fijo: tuple de string 'AAAA-MM-DD'
                       fechas de cortes fijos (no ajustables) de cambios de R0

            t_fijo: tuple de 2-tuples de strings
                    Rango donde se ajustará los cambios de R0
                
            Metodo: string
                    Metodo de optimización utilizado. La función ajusta un
                    modelo SEIR a los datos descargados. Valor por defecto 
                    "shgo". Valores posibles "dual_annealing""shgo", 
                    "brute" 
            
               
            
     retorna
         gráfico donde se representan cantidad casos confirmados y sus 
            ajustes por el modelo SEIR
                    
    Ejemplo
    >> t_lim_fijo=('2020-06-25',)
    >> t_lim=(('2020-08-01','2020-08-15'),)
    >> R0_fijo=(.85,) 
    >> R0_lim=((1.8,1.95),(1,1.2))
    
    >> FitSEIR(Provincia='Córdoba',fecha=('2020-04-01','2020-08-26'),R0_lim=R0_lim,
            R0_fijo=R0_fijo,t_lim=t_lim,t_lim_fijo=t_lim_fijo)
    
  
    
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
        Poblacion=load_fit_data_world(Pais)
       ########### Leer datos país ############################################
        DataC,DataR,DataM=readData(Pais)
        I0=DataC>0
        I=DataC.index>=fecha[0]
        II=DataC.index<=fecha[1]
        III=I0 & I & II
        tg1=pd.to_datetime(DataC[III].index)
        tg=pd.to_datetime(tg1).to_numpy()
        Ia=DataC[III].to_numpy()
        Id=DataC[III].diff().to_numpy()
        M_data=DataM[III].to_numpy()
        R_data=DataR[III].to_numpy()
        

        
        
        Ia=Ia/Poblacion #NOrmalizamos la poblacion total}
        
        
       
        M_data=M_data/Poblacion
        R_data=R_data/Poblacion
        
        
        #############   tiempo en días desde inicio
        t=np.arange(len(tg))

    else:
        if not dpto==None:
            Poblacion=load_fit_data_dpto(Provincia,dpto)
            Data=readDataArg_dpto(Provincia, dpto)
        else:
            Poblacion=load_fit_data(Provincia)
            Data=readDataArg(Provincia)
        
        tg1=pd.to_datetime(Data.index)
        
        I=tg1>=fecha[0]
        II=tg1<=fecha[1]
        III=I & II
        Data=Data[III]
        
        
        
        Ia=Data.CasosAcum.to_numpy()
        Id=Data.CasosDia.to_numpy()
        Ia=Ia/Poblacion #NOrmalizamos la poblacion total}
        tg=pd.to_datetime(Data.index).to_numpy()
        
        
        t=(tg-tg[0])/24.0/3600.0/1.0e9/np.timedelta64(1,'ns')
                   
    #### Rangos parametros fiteos
    
    t_ini=pd.to_datetime(fecha[0])
 
    
    t_corte_lim=()
    for t_lim_p in t_lim:
        t_lim1=(pd.to_datetime(t_lim_p[0])-t_ini).days
        t_lim2=(pd.to_datetime(t_lim_p[1])-t_ini).days
        t_corte_lim=t_corte_lim+((t_lim1,t_lim2),)
        
    t_lim_fijo=np.array([(pd.to_datetime(j)-t_ini).days for j in t_lim_fijo])
    
    R0_fijo=np.array(R0_fijo)
    
    
    rangos=t_corte_lim+R0_lim+((.0,1),)#elultimo ajusta la condicion inicial
    #es la proporcion de recuperados a los confirmados acumulados.
    ########### Condicion Inicial 
    
   
    
    
    ################Elegir el método  
      
    if Metodo=='dual_annealing':
        opt=scipy.optimize.dual_annealing(Error,rangos,args=(Ia,t,R0_fijo,t_lim_fijo))
        x_opt,error_opt=opt["x"],opt["fun"]
    elif Metodo=='shgo':
        opt=scipy.optimize.shgo(Error,rangos,args=(Ia,t,R0_fijo,t_lim_fijo))
        x_opt,error_opt=opt["x"],opt["fun"]
    elif Metodo=='brute':
        opt=scipy.optimize.brute(Error,rangos,args=(Ia,t,R0_fijo,t_lim_fijo),finish=None,full_output=True)
        x_opt,error_opt=opt[0:2]
    else:
        print("No existe el método"+Metodo )
        return
    
    
    
    
    
    ########### Exponiendo datos
    ### Extracción los resultados optimizacion
    
    Y0=[1-Ia[0],0.0,Ia[0]*x_opt[-1],Ia[0]*(1-x_opt[-1])]
    
    n=(len(x_opt[:-1])+1)/2
    t_corte_opt=np.concatenate([t_lim_fijo,x_opt[:n-1]])
    R0_opt=np.concatenate([R0_fijo,x_opt[n-1:-1]])
    
    ###  Calculo curva teórica resultante
    t_prediccion=365.0
    tt=np.arange(t_prediccion)
    t_tics=pd.Series(pd.date_range(str(tg[0]), freq='D', periods=t_prediccion))
    s=alpha*tt
    s_corte_opt=alpha*t_corte_opt
    sol =  odeint(SEIR,Y0 ,s, args=(s_corte_opt,R0_opt))
    S,E,I,R=sol[:,0],sol[:,1],sol[:,2],sol[:,3]
    
    ####  borrar era para hacer experimento
    #sol2 =  odeint(SEIR,Y0 ,s, args=([],[R0_opt[0]]))
    #S2,E2,I2,R2=sol2[:,0],sol2[:,1],sol2[:,2],sol2[:,3]    

    ##########################################################################
    ################## Creacion graficas######################################
    ##########################################################################

    fig = plt.figure(figsize=(14,10))
    
    
    ###  Grafica de infectados acumulados###################################
    ax = plt.axes()#[0.1, 0.1, 0.5, 0.8])
    
    ax.plot(t_tics.to_numpy(),(I+E+R)*Poblacion,tg,Ia*Poblacion,'o')
    
    #ax.plot(t_tics.to_numpy(),(I2+E2+R2)*Poblacion)#experimento
    
    
    ax.set(yscale='log')
    ax.set(ylim=(1,Poblacion))
    

    bottom, top = plt.ylim()  



    if Provincia==None: 
        ax.set_title(unicode(Pais,"utf-8")+"("+fecha[1]+")",fontsize=26)
    elif not dpto==None:
        ax.set_title("Departamento "+unicode(dpto,"utf-8")+"("+fecha[1]+")",fontsize=26)
    else:
        ax.set_title(unicode(Provincia,"utf-8")+"("+fecha[1]+")",fontsize=26)

    ax.legend(('I Modelo','I datos'),shadow=True, loc=(.0, .8),\
              handlelength=1.5, fontsize=12)
    
    
    ############### Infectados diarios ######################################
       
    
    Id_mod=k*Poblacion*E
    ax.plot(t_tics,Id_mod,tg,Id,'o')
    
    #Id_mod2=k*Poblacion*E2
    #ax.plot(t_tics,Id_mod2)#experimento
    
    ax.legend(('Modelo','Confirmados acumulados','Modelo', 'Confirmados diarios'),\
              shadow=True, loc=(.05, .82), handlelength=1.5, fontsize=12)
    
    ###############cortes
    
    t_corte_g=[]
    texto="R0 = %4.2f"%R0_opt[0]
    ax.text(t_tics[0],bottom+.1,texto)
    j=1
    for t in t_corte_opt:
        t_corte_g.append(tg[0]+np.timedelta64(int(t),'D'))
        ax.plot([t_corte_g[-1],t_corte_g[-1]],[0,top],color='black',linestyle='--')
        texto="R0 = %4.2f"%R0_opt[j]
        j=j+1
        ax.text(t_corte_g[-1],bottom+.1,texto)

    I_max=max(I)*Poblacion
    if len(t_corte_opt)>0:
        S0=S[int(t_corte_opt[-1])]
    else:
        S0=S[0]
    
    ##### Computamos relacion final
    f=lambda S_inf: np.log(S0/S_inf)-R0_opt[-1]*(1-S_inf)
    I_acum_inf=(1-scipy.optimize.fsolve(f,.000001))*Poblacion
    
    today = date.today()
    
    print "Fecha: "+str(today)
    
    formato=""
    for j in t_corte_opt:
        formato+="%s , "
    
    print "Tiempos de Corte ="+formato%tuple(str(i)[:10] for i in t_corte_g)
    
    
    formato=""
    for j in R0_opt:
        formato+="%10.2f , "
        
    tiempo_dupli=np.log(2.0)/np.log(R0_opt[-1])*(t_inf+t_exp)
    
 
    print "R0 = "+formato%tuple(R0_opt)
    print "t_inf = %10.2f"%t_inf+"d"
    print "t_exp = %10.2f"%t_exp+"d"
    print "I_max = %10.2e"%I_max+"h"
    print "Total Inf.= %10.2e"%I_acum_inf+"h"
    print "Tiempo duplicación actual=%10.2f"%tiempo_dupli+"d"
    H=np.sqrt(error_opt)*Poblacion
    print "error_out = %10.2e"%H
#  



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
    Ia,t,R0_fijo,t_lim_fijo=params
    Y0=[1-Ia[0],0.0,Ia[0]*x[-1],Ia[0]*(1-x[-1])]
    
    n=(len(x[:-1])+1)/2
    t_corte_aux,R0_aux=x[:n-1],x[n-1:-1]
    t_corte=np.concatenate([t_lim_fijo,t_corte_aux])
    R0=np.concatenate([R0_fijo,R0_aux])
   #Cambio escala tiempo
    s=t*alpha
    s_corte=alpha*t_corte
    Sol = odeint(SEIR,Y0 ,s, args=(s_corte,R0))
    return np.sum(((np.abs(Ia-Sol[:,2]-Sol[:,3]-Sol[:,1])))**2)



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
    DataC=DataC.loc[:,col].sum().rename('Confirmados')
    DataC.index=pd.to_datetime(DataC.index)
    
    
    col=DataM.columns[4:]
    DataM=DataM.loc[:,col].sum().rename('Muertes')
    DataM.index=pd.to_datetime(DataM.index)
   
    
    col=DataR.columns[4:]
    DataR=DataR.loc[:,col].sum().rename('Recuperados')
    DataR.index=pd.to_datetime(DataR.index)
    
    return DataC, DataM, DataR

##########################################################################
##################   Cargar rangos de ajuste, poblacion ##################
##########################################################################
####################   Paises ###############################################
def load_fit_data_world(Pais):
    """
    Carga la poblacion  desde el archivo 
    Data/Countries/countries.csv
    
    Parametros
              Pais: string, nombre del pais en ingles.
    Retorna:
            Poblacion: #habitantes, float 64
    """
    DataFitWorld=pd.read_csv('Data/Countries/countries.csv')
    I=DataFitWorld.Pais==Pais
    DataFit=DataFitWorld[I]
    Poblacion=DataFit.Poblacion[DataFit.index[0]]
    return Poblacion
    

###################  Provincias ##########################################
def load_fit_data(Provincia):
    """
    Carga solo la poblacvion del archivo 
    Data/Provincias/DataFitProv.csv
    
    Parametros
              Provincia: string, nombre de la provincia Argentina.
    Retorna:
            Poblacion: #habitantes, float 64
            
    """
    DataFitArg=pd.read_csv('Data/Provincias/DataFitProv.csv')
    I=DataFitArg.Provincia==Provincia
    DataFitProv=DataFitArg[I]
    Poblacion=DataFitProv.Poblacion[DataFitProv.index[0]]
    return float(Poblacion)
    
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
    return Poblacion
    




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
    os.rename(r'Data/Epidemic/Covid19Casos.csv',r'Data/Epidemic/Covid19CasosRespaldo.csv')
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
import os


###################  Variables Globales ######################################
t_inf=3.0 
t_exp=5.0
alpha=1.0/t_inf
k=1.0/t_exp
k_ast=k/alpha
epsilon=1.0
 

