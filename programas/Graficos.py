#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sun Jul  5 23:40:51 2020

@author: fernando
"""
import pandas as pd


########### Ejemplo 1, Grafico area de casos diarios y muertes###############

def EpiArg(provincia='Córdoba', dpto=None):
    Data=pd.read_csv('Data/Epidemic/Covid19Casos.csv')
    if not provincia=="Todas":
        Data=Data[Data.residencia_provincia_nombre==provincia]
    if not dpto==None:
        Data=Data[Data.residencia_departamento_nombre==dpto]
    DataC=Data[Data.clasificacion_resumen=='Confirmado']
    DataM=DataC[DataC.fallecido=='SI']
    
    J0=DataC[['id_evento_caso','fecha_apertura']].groupby('fecha_apertura')
    J1=J0.count().rename(columns={'id_evento_caso':'confirmado_diario'})
    H0=DataM[['id_evento_caso','fecha_fallecimiento']].groupby('fecha_fallecimiento')
    H1=H0.count().rename(columns={'id_evento_caso':'muertes_diarias'})
    H1.index=pd.to_datetime(H1.index)
    J1.index=pd.to_datetime(J1.index)
    
    H2=H1.cumsum().rename(columns={'muertes_diarias':'muertes_acumuladas'})
    J2=J1.cumsum().rename(columns={'confirmado_diario':'confirmados'})
    
    fig, ((ax1,ax2,ax3),(ax4,ax5,ax6)) = plt.subplots(2,3,figsize=(18,12))
    ax1.set_yscale('log')
    J2.plot.area(ax=ax1,legend=True)
    J1.plot.area(ax=ax1,legend=True)
    H2.plot.area(ax=ax1,legend=True)
    H1.plot.area(ax=ax1,legend=True)
    if dpto==None:
        ax1.set_title(unicode(provincia,"utf-8"),fontsize=18)
    else:
        ax1.set_title(unicode(provincia,"utf-8")+'-'+unicode(dpto,"utf-8")
        ,fontsize=18)


    ############# Ejemplo 2 Histogramas edades
    DataM.hist('edad',ax=ax2,bins=range(100))
    ax2.set_title(u"Distribución edad muertes",fontsize=18)
    #########3###Ejemplo 3, diagrama torta de sexos
    DataM.sexo.value_counts().plot.pie(ax=ax3)
    ax3.set_title(u"Distribución muertes por sexo",fontsize=18)
    
    
    #############  Ejemplo 4, Analisis de edad media muertes
    
    DataM_g=DataM.groupby('fecha_fallecimiento').mean()
    DataM_g.edad.plot(ax=ax4)
    DataM_g.edad.rolling(20, center=True).mean().plot(ax=ax4)
    ax4.set_title(u"Evolución edad media muertes",fontsize=18)
########## Ejemplo 5. Grafico area confirmados, 
### confirmados diarios y muertes globales

def EpiGlobal(Pais='Tierra'):
    DataC, DataM, DataR=readData(Pais)
    DataCd=DataC.diff().apply(abs).rename('Confirmados diarios')
    fig,ax=plt.subplots(figsize=(8,8))
    plt.yscale('log')
    DataC.plot.area(ax=ax,legend=True)
    DataCd.plot.area(ax=ax,legend=True)
    DataM.plot.area(ax=ax,legend=True)
    DataM.diff().apply(abs).rename('muertes_diarias').plot.area(ax=ax,legend=True)
    ax.set_title(unicode(Pais,"utf-8"),fontsize=18)
    
    
    
def MapaCOVID(provincia):
    """
        Hace un mapa de la provincia dividida por departamentos y colorea con 
        intensidades acorde a la cantidad de infectados totales de cada 
        departamento. 
    """
    
    campo='confirmado'
    
    
    if provincia=="AMBA":
        filepath4=dir1+"/Data/GeoData/AMBA.json"
        MapaProv=geopandas.read_file(filepath4)
        MapaProv.insert(9, "MuertesxInfectado", 0.0)
        MapaProv.index=MapaProv.in1
        DataProv=readDataArg('AMBA',campo=campo)       
    else:
        Arg=geopandas.read_file(filepath2)
        CodProv=str(codigo.Cod[provincia]).zfill(2)
        MapaProv=Arg[[h[:2]==CodProv for h in Arg['in1']]]
        MapaProv.insert(9, "MuertesxInfectado", 0.0)#isertar columna nueva
        MapaProv.index=MapaProv.in1
        DataProv=readDataArg(provincia,campo=campo)
        
    if len(DataProv)==0:
        return "No se registra"
    if provincia=="AMBA":
        CasosCABA=DataProv[DataProv.residencia_provincia_nombre=='CABA']
        Total=float(len(CasosCABA))
        H=CasosCABA.fallecido.value_counts()
        MapaProv.at['02',"MuertesxInfectado"]=float(H['SI'])/Total*100
        
        
        
        
        DataProv=DataProv[DataProv.residencia_provincia_id==6]
        DataProvM=DataProv[DataProv.fallecido=='SI']
        
        
        DataI=DataProv.residencia_departamento_id.value_counts()
        
        DataIM=DataProvM.residencia_departamento_id.value_counts()

        
        for h in DataIM.index:
            #if not(h==0):
            id='06'+str(h).zfill(3)
            MapaProv.at[id,"MuertesxInfectado"]=float(DataIM[h])/float(DataI[h])*100
    else:
        DataI=DataProv.residencia_departamento_id.value_counts()
        DataProvM=DataProv[DataProv.fallecido=='SI']
        DataIM=DataProvM.residencia_departamento_id.value_counts()
        for h in DataIM.index:
            #if not(h==0):
            id=CodProv+str(h).zfill(3)
            print(id)
            MapaProv.at[id,"MuertesxInfectado"]=float(DataIM[h])/float(DataI[h])*100
        
    fig, ax = plt.subplots(1, 1)
    divider = make_axes_locatable(ax)
    cax = divider.append_axes("right", size="5%", pad=0.1)
    MapaProv.plot(column='MuertesxInfectado',ax=ax,cax=cax,edgecolor="black",cmap=newcmp , legend=True)  
    ax.set_title(unicode(provincia,"utf-8"),fontsize=26)
    
    fig1, ax1 = plt.subplots(1, 1)
    
    Resultado=MapaProv.sort_values("MuertesxInfectado",ascending=False)
    Resultado.MuertesxInfectado.plot.bar(ax=ax1)
    return Resultado.nam

def readDataArg(provincia, campo=None):
    Data=pd.read_csv(filepath1)
    if campo=='confirmado':
        Data=Data[Data.clasificacion_resumen=="Confirmado"]
    if provincia=='AMBA':
        DataAMBA=geopandas.read_file(dir1+'/Data/GeoData/AMBA.json')
        #Primer datos es CABA lo leere de otra forma
        I1=[int(i[2:]) for i in DataAMBA.in1.values[1:]]
        I2=Data['residencia_provincia_id']==6
        I3=Data['residencia_departamento_id'].isin(I1)
        I4=Data['residencia_provincia_id']==2
        I= (I3 & I2) | I4 

        DataProv=Data.loc[I]
    else:
        CodProv=codigo.Cod[provincia]
        I=Data.residencia_provincia_id==CodProv 
        DataProv=Data[I] 
    return DataProv


#################  LIBRERIAS   ###############################################
import pandas as pd
import geopandas
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import make_axes_locatable
import os
from matplotlib import cm
from matplotlib.colors import ListedColormap
import numpy as np

#############  Nueva COLOR MAP ###############33
viridis = cm.get_cmap('Greens', 4096)
newcolors = viridis(np.linspace(0, 1, 4096))
white = np.array([.0, .0, .0, .0])
newcolors[:1, :] = white
newcmp = ListedColormap(newcolors)

##################  DIRECCIONES DE CARPETAS ###################################
dir1=unicode(os.getcwd(),'utf-8')
filepath1=dir1+"/Data/Epidemic/Covid19Casos.csv"
filepath2=dir1+"/Data/GeoData/departamento.json"
filepath3=dir1+"/Data/GeoData/provincia.json"


######################  CODIGOS DE provincia ##################################
codigo=pd.read_csv(dir1+'/Data/GeoData/CodProv.csv')
codigo.index=codigo.Provincia