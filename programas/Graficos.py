#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sun Jul  5 23:40:51 2020

@author: fernando
"""

Data=pd.read_csv(filepath1)
I1=Data.clasificacion_resumen=='Confirmado'
I2=Data.fallecido=='SI'
DataM=Data[I1 & I2]
DataC=Data[I1]
J=DataC[['id_evento_caso','fecha_apertura']].groupby('fecha_apertura').count().rename(columns={'id_evento_caso':'confirmado_diario'})
H=DataM[['id_evento_caso','fecha_fallecimiento']].groupby('fecha_fallecimiento').count().rename(columns={'id_evento_caso':'muertes_diarias'})
H.index=pd.to_datetime(H.index)
J.index=pd.to_datetime(J.index)
fig, axs = plt.subplots(figsize=(8,8))
plt.yscale('log')
J.plot.area(ax=axs)
H.plot.area(ax=axs)

fig1, axs1 = plt.subplots(figsize=(8,8))

DataM.hist('edad',bins=range(100))
DataM.sexo.value_counts().plot.pie(ax=axs1)


fig2, axs2 = plt.subplots(figsize=(8,8))
DataM_fe=DataM.fecha_fallecimiento.value_counts()
DataM_fe.sort_index().plot(Marker='o',ax=axs2)

fig3, axs3 = plt.subplots(figsize=(8,8))
DataM_g=DataM.groupby('fecha_fallecimiento').mean()
DataM_g.edad.rolling(20, center=True).mean().plot(ax=axs3)