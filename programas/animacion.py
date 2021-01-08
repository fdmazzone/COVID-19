#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sat Oct  3 19:00:31 2020

@author: fernando
"""

def MapaCOVID(Provincia, fecha):
    """
        Hace una animacion
    """
    
    
    ###################### CARGA MAPA ###################################
    if Provincia=="AMBA":
        MapaProv=geopandas.read_file("Data/GeoData/AMBA.json")
        MapaProv.insert(9, "Infectados", 0.0)
        MapaProv.index=MapaProv.in1
    elif Provincia=="Todas":
        MapaCABA=geopandas.read_file("Data/GeoData/AMBA.json").loc[0]
        MapaProv=geopandas.read_file("Data/GeoData/departamento.json")
        MapaProv=MapaProv[[not h[:2]=='02' for h in MapaProv.in1]]
        MapaCABA.in1='02000'
        MapaProv=MapaProv.append(MapaCABA)
        MapaProv.insert(9, "Infectados", 0.0)#isertar columna nueva
        MapaProv.index=MapaProv.in1
    else:
        Arg=geopandas.read_file("Data/GeoData/departamento.json")
        CodProv=str(codigo.Cod[Provincia]).zfill(2)
        MapaProv=Arg[[h[:2]==CodProv for h in Arg['in1']]]
        MapaProv.insert(9, "Infectados", 0.0)#isertar columna nueva
        MapaProv.index=MapaProv.in1

    ###################### CARGA DATOS #####################################
    DataProv=readDataArg(Provincia)
    I1=DataProv.fecha_apertura>=fecha[0]
    I2=DataProv.fecha_apertura<=fecha[1]
    DataProv=DataProv[I1 & I2]
    
    
#    if Provincia=="AMBA":
#        #DataProv[DataProv.residencia_provincia_nombre=='CABA']
#        CasosCABA=len(DataProv[DataProv.residencia_provincia_nombre=='CABA'])
#        MapaProv.at['02',"Infectados"]=CasosCABA
#        DataProv=DataProv[DataProv.residencia_provincia_id==6]
#        DataI=DataProv.residencia_departamento_id.value_counts()
#        for h in DataI.index:
#            #if not(h==0):
#            id='06'+str(h).zfill(3)
#            MapaProv.at[id,"Infectados"]=DataI[h]
#    elif Provincia=="Todas":
#        InfCABA=DataProv.residencia_provincia_nombre.value_counts()['CABA']
#        MapaProv.at['02000','Infectados']=InfCABA
#        I=[not h=='CABA' for h in DataProv.residencia_provincia_nombre]
#        DataProv=DataProv[I]
#        
#        I1=DataProv.residencia_provincia_id.apply(str).str.zfill(2)
#        I2=DataProv.residencia_departamento_id.apply(str).str.zfill(3)
#        DataProv.at[:,'id']=I1+I2
#        
#        DataI=DataProv.id.value_counts()
#    
#        for h in DataI.index:
#            MapaProv.at[h,"Infectados"]=DataI[h]
#      
#    else:
    
    ############   pARA OTRAS PROVINCIAS ESTO VENIA DESPUES DEL ELSE


    I=datetimeIterator(pd.to_datetime(fecha[0]),pd.to_datetime(fecha[1]))


    i=0
    for fecha_foto in I:
        MapaProv.loc[:,"Infectados"]=0.0
        I1=DataProv.fecha_apertura<=str(fecha_foto)[:10]
        DataI=DataProv[I1].residencia_departamento_id.value_counts()
        for h in DataI.index:
            id=CodProv+str(h).zfill(3)
            MapaProv.at[id,"Infectados"]=2*DataI[h]
        MapaProv_points = MapaProv.copy()
        MapaProv_points['geometry'] = MapaProv_points['geometry'].centroid       
        fig=plt.figure(figsize=(8,10))
        ax=fig.add_axes([0,0.01,1,.95])
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

def datetimeIterator(from_date=datetime.now(), to_date=None):
    while to_date is None or from_date <= to_date:
        yield from_date
        from_date = from_date + timedelta(days = 1)
    return

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