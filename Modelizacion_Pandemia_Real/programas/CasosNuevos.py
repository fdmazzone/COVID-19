#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sun Nov  1 21:17:06 2020

@author: fernando
"""
import pandas as pd
import numpy as np
def CasosNuevos(provincia='Todas', dpto=None):
    
    #Data=pd.read_csv('Data/Epidemic/Covid19Casos.csv')
    j=0
    L=np.array([0.0,0.0])
    for file in ['Data/Epidemic/Covid19Casos.csv','Data/Epidemic/Covid19Casos_viejo.csv']:
        chunk_size=1000000
        batch_no=1
        for chunk in pd.read_csv(file,chunksize=chunk_size):
            print(batch_no)
            A=chunk[chunk.clasificacion_resumen=='Confirmado']
            if not provincia=="Todas":
                A=A[A.residencia_provincia_nombre==provincia]
            if not dpto==None:
                A=A[A.residencia_departamento_nombre==dpto]
            batch_no+=1
            L[j]+=len(A)
        j+=1
    
    dif=L[0]-L[1]
    return dif