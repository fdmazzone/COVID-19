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
    CodProv=str(codigo.Cod[Provincia]).zfill(2)
    MapaProv=Arg[[h[:2]==CodProv for h in Arg['in1']]]
    MapaProv.insert(9, "Infectados", 0.0)#isertar columna nueva
    MapaProv.index=MapaProv.in1
    
    DataProv,fecha=readDataArg(Provincia,campo='confirmado')
    if len(DataProv)==0:
        return "No se registra"
    if dia:
        I=DataProv.fecha_apertura==fecha
        DataProv=DataProv[I]
        if len(DataProv)==0:
            return "No se registra"

    DataI=DataProv.residencia_departamento_id.value_counts()
    fig, ax = plt.subplots(1, 1)
    divider = make_axes_locatable(ax)
    cax = divider.append_axes("right", size="5%", pad=0.1)
    
    for h in DataI.index:
        #if not(h==0):
        id=CodProv+str(h).zfill(3)
        MapaProv.at[id,"Infectados"]=DataI[h]
    

    MapaProv.plot(column='Infectados',ax=ax,cax=cax,edgecolor="black",cmap='YlGn', legend=True)  
    ax.set_title(unicode(Provincia,"utf-8"),fontsize=26)
    
    fig1, ax1 = plt.subplots(1, 1)
    
    Resultado=MapaProv.sort_values("Infectados",ascending=False)
    Resultado.Infectados.plot.bar(ax=ax1)
    return Resultado.nam

def MapaTest(Provincia, dia=False):
    """
        Hace un mapa de la provincia dividida por departamentos y colorea con 
        intensidades acorde a la cantidad de infectados totales de cada 
        departamento. 
    """
    
    Arg=geopandas.read_file(filepath2)
    
  
    CodProv=str(codigo.Cod[Provincia]).zfill(2)
    MapaProv=Arg[[h[:2]==CodProv for h in Arg['in1']]]
    MapaProv.insert(9, "Infectados", 0.0)#isertar columna nueva
    MapaProv.index=MapaProv.in1
    
    DataProv,fecha=readDataArg(Provincia)
    if len(DataProv)==0:
        return "No se registra"
    if dia:
        I=DataProv.fecha_apertura==fecha
        DataProv=DataProv[I]
        if len(DataProv)==0:
            return "No se registra"

    DataI=DataProv.residencia_departamento_id.value_counts()
    fig, ax = plt.subplots(1, 1)
    divider = make_axes_locatable(ax)
    cax = divider.append_axes("right", size="5%", pad=0.1)
    
    for h in DataI.index:
        #if not(h==0):
        id=CodProv+str(h).zfill(3)
        MapaProv.at[id,"Infectados"]=DataI[h]
    

    MapaProv.plot(column='Infectados',ax=ax,cax=cax,edgecolor="black",cmap='YlGn', legend=True)  
    ax.set_title(unicode(Provincia,"utf-8"),fontsize=26)
    
    fig1, ax1 = plt.subplots(1, 1)
    
    Resultado=MapaProv.sort_values("Infectados",ascending=False)
    Resultado.Infectados.plot.bar(ax=ax1)
    return Resultado.nam

def readDataArg(Provincia, campo=None):
    Data=pd.read_csv(filepath1)   
    fecha=Data.ultima_actualizacion[0]
    I=Data.residencia_provincia_nombre==Provincia 
    if campo=='confirmado':
        I1=Data.clasificacion_resumen=="Confirmado"
        I=I & I1
    DataProv=Data[I] 
    return DataProv, fecha


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



