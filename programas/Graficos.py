#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sun Jul  5 23:40:51 2020

@author: fernando
"""
import pandas as pd


########### Ejemplo 1, Grafico area de casos diarios y muertes###############
Data=pd.read_csv('Data/Epidemic/Covid19Casos.csv')
Data=Data[Data.residencia_provincia_nombre=='Córdoba']
I1=Data.clasificacion_resumen=='Confirmado'
I2=Data.fallecido=='SI'
DataM=Data[I1 & I2]
DataC=Data[I1]
J0=DataC[['id_evento_caso','fecha_apertura']].groupby('fecha_apertura')
J1=J0.count().rename(columns={'id_evento_caso':'confirmado_diario'})
H0=DataM[['id_evento_caso','fecha_fallecimiento']].groupby('fecha_fallecimiento')
H1=H0.count().rename(columns={'id_evento_caso':'muertes_diarias'})
H1.index=pd.to_datetime(H1.index)
J1.index=pd.to_datetime(J1.index)
fig, axs = plt.subplots(figsize=(8,8))
plt.yscale('log')
J1.plot(ax=axs,Marker='o')
H1.plot(ax=axs,Marker='o')


############# Ejemplo 2 Histogramas edades
DataM.hist('edad',bins=range(100))

#########3###Ejemplo 3, diagrama torta de sexos
DataM.sexo.value_counts().plot.pie()



#############  Ejemplo 4, Analisis de edad media muertes
fig3, axs3 = plt.subplots(figsize=(8,8))
DataM_g=DataM.groupby('fecha_fallecimiento').mean()
DataM_g.edad.plot(ax=axs3)
DataM_g.edad.rolling(20, center=True).mean().plot(ax=axs3)

########## Ejemplo 5. Grafico area confirmados, 
### confirmados diarios y muertes globales
DataC, DataM, DataR=readData('Denmark')
DataCd=DataC.diff().apply(abs).rename('Confirmados diarios')
fig,ax=plt.subplots(figsize=(8,8))
plt.yscale('log')
DataC.plot.area(ax=ax,legend=True)
DataCd.plot.area(ax=ax,legend=True)
DataM.plot.area(ax=ax,legend=True)