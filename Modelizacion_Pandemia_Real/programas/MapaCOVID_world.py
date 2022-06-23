#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Dec 13 11:50:01 2020

@author: fernando

x264 out.mp4
"""


################### FUNCIONES ###############################################
def MapaCOVID(fecha):
    """
        Hace una animacion
    """
    mapa_world = geopandas.read_file(geopandas.datasets.get_path('naturalearth_lowres'))
    mapa_world.index=mapa_world.name
    mapa_world.insert(6, "Infectados", 0.0)
    
    for Pais in mapa_world.index:
        if Pais=='United States of America':
            DataC=readData('US')[0]
        else:
            DataC=readData(Pais)[0]
        Inf1=DataC[pd.to_datetime(fecha[0])]
        Inf2=DataC[pd.to_datetime(fecha[1])]
        DeltaInf=Inf2-Inf1
        Poblacion=mapa_world.loc[Pais].pop_est
            
            
            
        mapa_world.at[Pais,"Infectados"]=(1.0/Poblacion)*1e6*DeltaInf
    
    fig=plt.figure(figsize=(30,15))
    ax=fig.add_axes([0.05,0.05,.9,.9])
    ax.set_aspect(aspect=1.0)    
    divider = make_axes_locatable(ax)
    cax = divider.append_axes("right", size="2%", pad=0.1)
    mapa_world.plot(column='Infectados',ax=ax,cax=cax,edgecolor="black",
                  cmap=newcmp , legend=True)  

    return fig, ax
    
    
    
    
    
    
    
    
    
    
    
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

#################  LIBRERIAS   ###############################################
import pandas as pd
import geopandas
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import make_axes_locatable
from matplotlib import cm
from matplotlib.colors import ListedColormap
import numpy as np
#from shapely.geometry import Point, Polygon

################# Vriables Globales ##########################################

#############  Nueva COLOR MAP ###############33
viridis = cm.get_cmap('Oranges', 4096)
newcolors = viridis(np.linspace(0, 1, 4096))
white = np.array([.0, .0, .0, .0])
newcolors[:1, :] = white
newcmp = ListedColormap(newcolors**5)

