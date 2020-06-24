#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon Jun 15 14:04:23 2020

@author: Fernando Mazzone
"""



def MapaContagios(Provincia, dia=False):
    """
        Hace un mapa de la provincia dividida por departamentos y colorea con 
        intensidades acorde a la cantidad de infectados totales de cada 
        departamento. 
    """
    
    Arg=geopandas.read_file(filepath2)
    
    CABA=False
    if Provincia=="Buenos Aires-CABA":
        Provincia="Buenos Aires" 
        CABA=True
    CodProv=str(codigo.Cod[Provincia]).zfill(2)
    MapaProv=Arg[[h[:2]==CodProv for h in Arg['in1']]]
    MapaProv.insert(9, "Infectados", 0.0)#isertar columna nueva
    MapaProv.index=MapaProv.in1
    
    DatosProv=readDataArg(Provincia)
    if not dia:
        DataProv=DatosProv[0]
    else:
        DataProv=DatosProv[1]
    DataI=DataProv.residencia_departamento_id.value_counts()
    fig, ax = plt.subplots(1, 1)
    divider = make_axes_locatable(ax)
    cax = divider.append_axes("right", size="5%", pad=0.1)
    
    for h in DataI.index:
        #if not(h==0):
        id=CodProv+str(h).zfill(3)
        MapaProv.at[id,"Infectados"]=DataI[h]
    

    
    if CABA:
        DataCABA=readDataArg('CABA')
        InfCABA=DataCABA.residencia_provincia_id.value_counts()[2]
        MapaCABA=geopandas.read_file(filepath3).drop(columns='entidad').head(1)
        MapaCABA.insert(9, "Infectados", InfCABA)
        MapaProv=pd.concat([MapaProv, MapaCABA])
        
    
    MapaProv.plot(column='Infectados',ax=ax,cax=cax,edgecolor="black",cmap='YlGn', legend=True)  
    ax.set_title(unicode(Provincia,"utf-8"),fontsize=26)
    
    fig1, ax1 = plt.subplots(1, 1)
    
    Resultado=MapaProv.sort_values("Infectados",ascending=False)
    Resultado.Infectados.plot.bar(ax=ax1)
    return Resultado.nam



def readDataArg(Provincia):
    Data=pd.read_csv(filepath1)   
    I1=Data.residencia_provincia_nombre==Provincia   
    I2=Data.clasificacion_resumen=="Confirmado" 
    DataProv=Data[I2 & I1] 
    CasosDia=DataProv.fecha_apertura.value_counts()
    #CasosDia=DataProv.fecha_inicio_sintomas.value_counts()
    IndF=DataProv.fecha_apertura.index[-1]
    DataProvD=DataProv[DataProv.fecha_apertura==DataProv.fecha_apertura[IndF]]
    return DataProv, DataProvD


#################  LIBRERIAS   ###############################################
import pandas as pd
import geopandas
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import make_axes_locatable
import os


##################  DIRECCIONES DE CARPETAS ###################################
dir1=unicode(os.getcwd(),'utf-8')


filepath1=dir1+"/Data/Epidemic/Covid19Casos.csv"
filepath2=dir1+"/Data/GeoData/departamento.json"
filepath3=dir1+"/Data/GeoData/provincia.json"


######################  CODIGOS DE PROVINCIA ##################################
codigo=pd.read_csv(dir1+'/Data/GeoData/CodProv.csv')
codigo.index=codigo.Provincia



