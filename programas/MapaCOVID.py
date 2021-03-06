#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon Jun 15 14:04:23 2020

@author: Fernando Mazzone
"""



def MapaCOVID(Provincia="Todas",tipo="burbuja", fecha=None
              ,capa=None,densidad=None):
    """
        Hace un mapa de la provincia dividida por departamentos en indica 
        cantidad de casos confirmados con diagramas de burbuja o con un 
        mapa colorpléctico. 
        
        Parametros: Provincia: str. Nombre de una provincia Argentina
                    
                    
                    tipo: str. Tipo del gráfico "burbuja" o "colorpléctico".
                    Valor por defecto "Burbuja"
                    
                    fecha: tuple o None. Si fecha = None se consideran todos 
                    los casos, si fecha=("AAAA-MM-DD", "aaaa-mm-dd") se 
                    consideran los casos de entre las fechas estipuladas.
                    Debe ser "AAAA-MM-DD"<= "aaaa-mm-dd". Valor por defecto 
                    None.
        retorna: Mapa con distribución de casos 
    """
    
    DataProv=readDataArg(Provincia)
    
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

    
    if len(DataProv)==0:
        return "No se registra"

    if not fecha==None:
        I1=DataProv.fecha_apertura>=fecha[0]
        I2=DataProv.fecha_apertura<=fecha[1]
        DataProv=DataProv[I1 & I2]
        if len(DataProv)==0:
            return "No se registra"
    if Provincia=="AMBA":
        #DataProv[DataProv.residencia_provincia_nombre=='CABA']
        CasosCABA=len(DataProv[DataProv.residencia_provincia_nombre=='CABA'])
        MapaProv.at['02',"Infectados"]=CasosCABA
        DataProv=DataProv[DataProv.residencia_provincia_id==6]
        DataI=DataProv.residencia_departamento_id.value_counts()
        for h in DataI.index:
            #if not(h==0):
            id='06'+str(h).zfill(3)
            MapaProv.at[id,"Infectados"]=DataI[h]
    elif Provincia=="Todas":
        InfCABA=DataProv.residencia_provincia_nombre.value_counts()['CABA']
        if not densidad==None:
            MapaProv.at['02000','Infectados']=InfCABA/3075646.0*densidad
        else:
            MapaProv.at['02000','Infectados']=InfCABA
        I=[not h=='CABA' for h in DataProv.residencia_provincia_nombre]
        DataProv=DataProv[I]
        
        I1=DataProv.residencia_provincia_id.apply(str).str.zfill(2)
        I2=DataProv.residencia_departamento_id.apply(str).str.zfill(3)
        DataProv.at[:,'id']=I1+I2
        
        DataI=DataProv.id.value_counts()
    
        if not densidad==None:
            Data_dpto=pd.read_csv('Data/Poblacion/poblacion_dpto.csv')
            for h in DataI.index:
                ind_dpto=int(h)
                if ind_dpto in Data_dpto.in1.to_numpy(): #hay departamentos con 
                    #codigos erroneos en la base del ministerio de salud
                    J=Data_dpto[Data_dpto.in1==ind_dpto]
                    hab=float(J.personas.loc[J.index[0]])
                    MapaProv.at[h,"Infectados"]=DataI[h]/hab*densidad
        else:
            for h in DataI.index:
                MapaProv.at[h,"Infectados"]=DataI[h]

        
    else:
        DataI=DataProv.residencia_departamento_id.value_counts()
        for h in DataI.index:
            id=CodProv+str(h).zfill(3)
            MapaProv.at[id,"Infectados"]=DataI[h]
    
    MapaProv_points = MapaProv.copy()
    MapaProv_points['geometry'] = MapaProv_points['geometry'].centroid
    
    fig=plt.figure(figsize=(10,14))
    ax=fig.add_axes([0,0.05,1,.85])
    ax.set_aspect(aspect=1.0)

    if tipo=='colorpléctico':
        divider = make_axes_locatable(ax)
        cax = divider.append_axes("right", size="5%", pad=0.1)
        MapaProv.plot(column='Infectados',ax=ax,cax=cax,edgecolor="black",
                      cmap=newcmp , legend=True)  
        if Provincia=="Todas":
            MapaProv2=geopandas.read_file('Data/GeoData/provincia.json')
            MapaProv2.plot(ax=ax, color="white",alpha=.1, edgecolor="black", linewidth=5.0)
            ax.set_ylim(-55.13, -21.2);ax.set_xlim(-73.8, -53.27)
            ax.set_aspect(aspect=.97)
        else:
            MapaProv.plot(ax=ax, color="white", edgecolor="grey", linewidth=0.4)
            if Provincia=="Todas":
                MapaProv2=geopandas.read_file('Data/GeoData/provincia.json')
                Prov_cont=MapaProv2.plot(ax=ax, color="white",alpha=.1, edgecolor="black", linewidth=5.0)
                ax.set_ylim(-55.13, -21.2);ax.set_xlim(-73.8, -53.27)
            MapaProv_points.Infectados=5000*MapaProv_points.Infectados/MapaProv_points.Infectados.max()
            MapaProv_points.plot(ax=ax,color="#e63131", markersize="Infectados",
                                 alpha=0.7, categorical=False, legend=True )

    if not Provincia=="Todas":
        for x, y, label in zip(MapaProv_points.geometry.x,
                               MapaProv_points.geometry.y, MapaProv_points.in1):
            ax.annotate(label, xy=(x, y),color='blue', xytext=(2, 2), fontsize=8,textcoords="offset points")
 
    if capa=='localidades' and not Provincia=='AMBA':
        Localidades=pd.read_csv("Data/GeoData/municipios.csv")
        if not Provincia=='Todas':
            Localidades=Localidades[Localidades.provincia_nombre==Provincia]
        for  h in Localidades.index:
            x=Localidades.centroide_lat[h]
            y=Localidades.centroide_lon[h]
            label=Localidades.nombre[h]
            ax.annotate(label, xy=( y,x),color='black', xytext=(2, 2), fontsize=8,textcoords="offset points")
            ax.scatter(y,x,color='black')


    
    if Provincia=="Todas":
        titulo="Argentina"+"("+fecha[0]+" , "+fecha[1]+")"
    else:
        titulo=Provincia+"("+fecha[0]+" , "+fecha[1]+")"
    
    ax.set_title(titulo,fontsize=18)
    
        
    
    
    
    #fig1, ax1 = plt.subplots(figsize=(12,12))
    
    #Resultado=MapaProv.sort_values("Infectados",ascending=False)
    #Resultado.Infectados.plot.bar(ax=ax1)
    return fig, ax

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



######################  CODIGOS DE PROVINCIA ##################################
codigo=pd.read_csv('Data/GeoData/CodProv.csv')
codigo.index=codigo.Provincia

#MapaCOVID(Provincia="La Pampa",campo='confirmado',fecha=('2020-08-01','2020-08-01'),capa='localidades')


