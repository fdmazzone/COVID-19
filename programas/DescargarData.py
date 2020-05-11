#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Descarga datos actuales de internet  desde John Hopskins y otros sitios
Cambiar la variable MiDirectorio con el directorio que se desaea trabajar
@author: Fernando Mazzone
"""
import requests



MiDirectorio='/home/fernando/fer/Investigación/Trabajo en curso/COVID-19/programas/'


urlb='https://data.humdata.org/hxlproxy/api/data-preview.csv?url=https%3A%2F%2Fraw.githubusercontent.com%2FCSSEGISandData%2FCOVID-19%2Fmaster%2Fcsse_covid_19_data%2Fcsse_covid_19_time_series%2F'
url1 = 'time_series_covid19_confirmed_global.csv&filename=time_series_covid19_confirmed_global.csv'
url2 = 'time_series_covid19_deaths_global.csv&filename=time_series_covid19_deaths_global.csv'
url3 = 'time_series_covid19_recovered_global.csv&filename=time_series_covid19_recovered_global.csv'



urlUSA = 'https://covidtracking.com/api/v1/us/daily.csv'

myfile = requests.get(urlUSA)
open(MiDirectorio+'DataUSA.csv', 'wb').write(myfile.content)


myfile = requests.get(urlb+url1)
open(MiDirectorio+'DataConfirmados.csv', 'wb').write(myfile.content)

myfile = requests.get(urlb+url2)
open(MiDirectorio+'DataMuertos.csv', 'wb').write(myfile.content)

myfile = requests.get(urlb+url3)
open(MiDirectorio+'DataRecuperados.csv', 'wb').write(myfile.content)
