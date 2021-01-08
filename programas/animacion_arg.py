#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sat Oct  3 19:00:31 2020

@author: fernando

Usar ImageMsagick 
convert -delay 50 *.png ARGSemanales.mp4

"""

#################  LIBRERIAS   ###############################################
import pandas as pd
import geopandas
import matplotlib.pyplot as plt
#from mpl_toolkits.axes_grid1 import make_axes_locatable
from matplotlib import cm
import numpy as np
#from shapely.geometry import Point, Polygon
from datetime import datetime,timedelta


################# Vriables Globales ##########################################



######################  CODIGOS DE PROVINCIA ##################################
codigo=pd.read_csv('Data/GeoData/CodProv.csv')
codigo.index=codigo.Provincia

def AnimacionARG(fecha):
    """
        Hace una animacion
    """
    
    
    ###################### CARGA MAPA ###################################
    MapaCABA=geopandas.read_file("Data/GeoData/AMBA.json").loc[0]
    MapaProv=geopandas.read_file("Data/GeoData/departamento.json")
    MapaProv=MapaProv[[not h[:2]=='02' for h in MapaProv.in1]]
    MapaCABA.in1='02000'
    MapaProv=MapaProv.append(MapaCABA)
    MapaProv.insert(9, "Infectados", 0.0)#isertar columna nueva
    MapaProv.index=MapaProv.in1

    ###################### CARGA DATOS #####################################
    DataProv=readDataArg("Todas")
    I1=DataProv.fecha_apertura>=fecha[0]
    I2=DataProv.fecha_apertura<=fecha[1]
    DataProv=DataProv[I1 & I2]
    
    
    step=7
    I=datetimeIterator(pd.to_datetime(fecha[0]),pd.to_datetime(fecha[1]),step=step)

    factor=.4
    i=36
    for fecha_foto in I:
        MapaProv.loc[:,"Infectados"]=0.0
        I1=DataProv.fecha_apertura<str(fecha_foto+timedelta(days = step))[:10]
        I2=DataProv.fecha_apertura>=str(fecha_foto)[:10]
        DataFecha=DataProv[I1 & I2]
        InfCABA=DataFecha.residencia_provincia_nombre.value_counts()['CABA']
        
        MapaProv.at['02000','Infectados']=factor*InfCABA
        I=[not h=='CABA' for h in DataFecha.residencia_provincia_nombre]
        DataFecha=DataFecha[I]
        I1=DataFecha.residencia_provincia_id.apply(str).str.zfill(2)
        I2=DataFecha.residencia_departamento_id.apply(str).str.zfill(3)
        DataFecha.loc[:,'id']=I1+I2
        DataI=DataFecha.id.value_counts()
    
        for h in DataI.index:
            MapaProv.at[h,"Infectados"]=factor*DataI[h]
      
        

        MapaProv_points = MapaProv.copy()
        MapaProv_points['geometry'] = MapaProv_points['geometry'].centroid       
        fig=plt.figure(figsize=(6,10))
        ax=fig.add_axes([0,0.01,1,.95])
        ax.set_ylim(-55.13, -21.2);ax.set_xlim(-73.8, -53.27)
        # region centro ax.set_ylim(-35.3, -30.5);ax.set_xlim(-65.5, -57.6)
        MapaProv.plot(ax=ax, color="white", edgecolor="grey", linewidth=2)
        MapaProv_points.plot(ax=ax,color="#e63131", markersize="Infectados",
                             alpha=0.7, categorical=False, legend=True )
    
        titulo=str(fecha_foto)[:10]
       
        file_name=str(i).zfill(3)+'.png'
        ax.set_title(titulo,fontsize=20)
        ax.axes.xaxis.set_visible(False)
        ax.axes.yaxis.set_visible(False)
        plt.savefig(file_name)
        plt.close()
        i=i+1
        
    return []
    
    

def readDataArg(Provincia):
    """
    Lee datos de la base descargada del ministerio de salud de la República 
    Argentina.
    
    Parametros:
            Provincia: string, provincia Argentina.
    retorna:
           Pandas DataFrame. con todos las columnas de la base original.
    """
    
    
    Data=pd.read_csv("Data/Epidemic/Covid19Casos.csv")
    Data=Data[Data.clasificacion_resumen=="Confirmado"]
    if Provincia=='AMBA':
        DataAMBA=geopandas.read_file('Data/GeoData/AMBA.json')
        #Primer datos es CABA lo leere de otra forma
        I1=[int(i[2:]) for i in DataAMBA.in1.values[1:]]
        I2=Data['residencia_provincia_id']==6
        I3=Data['residencia_departamento_id'].isin(I1)
        I4=Data['residencia_provincia_id']==2
        I= (I3 & I2) | I4 

        DataProv=Data.loc[I]
    elif Provincia=="Todas":
        DataProv=Data
    else:
        CodProv=codigo.Cod[Provincia]
        I=Data.residencia_provincia_id==CodProv 
        DataProv=Data[I] 
    return DataProv

def datetimeIterator(from_date=datetime.now(), to_date=None,step=1):
    while to_date is None or from_date <= to_date:
        yield from_date
        from_date = from_date + timedelta(days = step) #saltos de 7 dias
    return 

