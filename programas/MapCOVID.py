#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon Jun 15 14:04:23 2020

@author: Fernando Mazzone
"""



def MapaCOVID(Provincia,campo=None, fecha=None):
    """
        Hace un mapa de la provincia dividida por departamentos y colorea con 
        intensidades acorde a la cantidad de infectados totales de cada 
        departamento. 
    """
    
    
    
    if Provincia=="AMBA":
        filepath4=dir1+"/Data/GeoData/AMBA.json"
        MapaProv=geopandas.read_file(filepath4)
        MapaProv.insert(9, "Infectados", 0.0)
        MapaProv.index=MapaProv.in1
        DataProv=readDataArg('AMBA',campo=campo)       
    else:
        Arg=geopandas.read_file(filepath2)
        CodProv=str(codigo.Cod[Provincia]).zfill(2)
        MapaProv=Arg[[h[:2]==CodProv for h in Arg['in1']]]
        MapaProv.insert(9, "Infectados", 0.0)#isertar columna nueva
        MapaProv.index=MapaProv.in1
        DataProv=readDataArg(Provincia,campo=campo)
        
    if len(DataProv)==0:
        return "No se registra"

    if not fecha==None:
        I=DataProv.fecha_apertura==fecha
        DataProv=DataProv[I]
        if len(DataProv)==0:
            return "No se registra"
    if Provincia=="AMBA":
        DataProv[DataProv.residencia_provincia_nombre=='CABA']
        CasosCABA=len(DataProv[DataProv.residencia_provincia_nombre=='CABA'])
        MapaProv.at['02',"Infectados"]=CasosCABA
        DataProv=DataProv[DataProv.residencia_provincia_id==6]
        DataI=DataProv.residencia_departamento_id.value_counts()
        for h in DataI.index:
            #if not(h==0):
            id='06'+str(h).zfill(3)
            MapaProv.at[id,"Infectados"]=DataI[h]
    else:
        DataI=DataProv.residencia_departamento_id.value_counts()
        for h in DataI.index:
            #if not(h==0):
            id=CodProv+str(h).zfill(3)
            MapaProv.at[id,"Infectados"]=DataI[h]
        
    fig, ax = plt.subplots(1, 1)
    divider = make_axes_locatable(ax)
    cax = divider.append_axes("right", size="5%", pad=0.1)
    MapaProv.plot(column='Infectados',ax=ax,cax=cax,edgecolor="black",cmap=newcmp , legend=True)  
    ax.set_title(unicode(Provincia,"utf-8"),fontsize=26)
    
    fig1, ax1 = plt.subplots(1, 1)
    
    Resultado=MapaProv.sort_values("Infectados",ascending=False)
    Resultado.Infectados.plot.bar(ax=ax1)
    return Resultado.nam

def readDataArg(Provincia, campo=None):
    Data=pd.read_csv(filepath1)
    if campo=='confirmado':
        Data=Data[Data.clasificacion_resumen=="Confirmado"]
    if Provincia=='AMBA':
        DataAMBA=geopandas.read_file(dir1+'/Data/GeoData/AMBA.json')
        #Primer datos es CABA lo leere de otra forma
        I1=[int(i[2:]) for i in DataAMBA.in1.values[1:]]
        I2=Data['residencia_provincia_id']==6
        I3=Data['residencia_departamento_id'].isin(I1)
        I4=Data['residencia_provincia_id']==2
        I= (I3 & I2) | I4 

        DataProv=Data.loc[I]
    else:
        CodProv=codigo.Cod[Provincia]
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
newcmp = ListedColormap(newcolors**5)

##################  DIRECCIONES DE CARPETAS ###################################
dir1=unicode(os.getcwd(),'utf-8')
filepath1=dir1+"/Data/Epidemic/Covid19Casos.csv"
filepath2=dir1+"/Data/GeoData/departamento.json"
filepath3=dir1+"/Data/GeoData/provincia.json"


######################  CODIGOS DE PROVINCIA ##################################
codigo=pd.read_csv(dir1+'/Data/GeoData/CodProv.csv')
codigo.index=codigo.Provincia



