#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Dec 13 08:59:03 2020

@author: fernando

para convertir a video usar

ffmpeg -framerate 1 -pattern_type glob -i '*.png' -c:v lib
"""


#################  LIBRERIAS   ###############################################
import pandas as pd
import geopandas
import matplotlib.pyplot as plt
#from mpl_toolkits.axes_grid1 import make_axes_locatable
from matplotlib import cm
import numpy as np
from shapely.geometry import Point, Polygon
from datetime import datetime,timedelta


################# Vriables Globales ##########################################



def MapaCOVID(fecha):
    """
        Hace una animacion
    """
    mapa_world = geopandas.read_file(geopandas.datasets.get_path('naturalearth_lowres'))
    mapa_world.index=mapa_world.name
    mapa_world_points = mapa_world.copy()
    mapa_world_points['geometry'] = mapa_world_points['geometry'].centroid
    mapa_world_points.at['United States of America','geometry']=Point (-94.639816,38.207188)
    mapa_world_points.at['France','geometry']=Point (3.4357191,46.567395)
    mapa_world_points.insert(6, "Infectados", 0.0)
    
    
    I=datetimeIterator(pd.to_datetime(fecha[0]),pd.to_datetime(fecha[1]))


    i=100
    for fecha_foto in I:
        
        
        for Pais in mapa_world.index:
            Poblacion=mapa_world.loc[Pais].pop_est
            if Pais=='United States of America':
                DataC=readData('US')[0]
            else:
                DataC=readData(Pais)[0]
            fecha_foto2=fecha_foto+timedelta(days = 7)
            DeltaInf=DataC[fecha_foto2]-DataC[fecha_foto]
            #DeltaInf=DataC[fecha_foto]
            #acumulados
            #mapa_world_points.at[Pais,"Infectados"]=DeltaInf/500.0
            mapa_world_points.at[Pais,"Infectados"]=DeltaInf*(1.0/Poblacion)*1.0e6
        fig=plt.figure(figsize=(30,15))
        ax=fig.add_axes([0,0.01,1,.95])
        mapa_world.plot(ax=ax, color="white", edgecolor="grey", linewidth=2)
        mapa_world_points.plot(ax=ax,color="#e63131", markersize="Infectados",
                                 alpha=0.7, categorical=False, legend=True )
        file_name=str(i).zfill(3)+'.png'
        titulo=str(fecha_foto)[:10]
        ax.set_title(titulo,fontsize=20)
        ax.axes.xaxis.set_visible(False)
        ax.axes.yaxis.set_visible(False)
        plt.savefig(file_name)
        plt.close()
        i=i+1
   



################### FUNCIONES ###############################################
def datetimeIterator(from_date=datetime.now(), to_date=None):
    while to_date is None or from_date <= to_date:
        yield from_date
        from_date = from_date + timedelta(days = 7)
    return

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
