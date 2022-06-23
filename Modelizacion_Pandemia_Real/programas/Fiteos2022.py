#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov 29 15:33:26 2021

@author: fernando
"""
from FitSEIR import *
from datetime import date, timedelta

hoy=str(date.today())
 


dir_fiteo_prov="/home/fernando/fer/Investigacion/Trabajo_en_curso/COVID-19/Modelizacion_Pandemia_Real/COVID-19-WEB/fiteos/imagenes/"










FitSEIR(Pais='Argentina',fecha=('2021-10-01',hoy),R0_lim=((0.5,2),),\
        R0_fijo=(),Metodo='dual_annealing',Rango_I0=((.001,.1),),save=dir_fiteo_prov)

FitSEIR(Pais='Argentina',Data=Data,Provincia="Córdoba",fecha=('2021-10-01',hoy),R0_lim=((0.5,2),),\
        R0_fijo=(),Metodo='dual_annealing',Rango_I0=((.001,.1),),save=dir_fiteo_prov)    
