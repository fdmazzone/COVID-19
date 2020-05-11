#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Thu May  7 08:02:17 2020

@author: fernando

Los primeros 4 items de la fila son vacio,
nombre del país, lat, long. No los usamos
OJO: en los datos de la tabla hay valores acumulados de infectados, en los modelos
cuentan los  infectados activos 
Infectados Activos= Infectados Acumulados-(muertos+recuperados)

S_data,I_data,M_data,R_data=ExtraerDatos(IndPais,Poblacion)
IndPais = Fila del pais-región
Poblacion=Total de habitantes
S_data,I_data,M_data,R_data Datos de Susceptibles, infecciosos, muertes y recuperados
"""

import csv
def ExtraerDatos(Pais,Poblacion):
    if Pais=='USA':
        I_data_acum=np.array([])
        I_data=np.array([])
        M_data=np.array([])
        R_data=np.array([])
        S_data=np.array([])

        with open('DataUSA.csv') as csvfile:
            reader = csv.reader(csvfile)
            next(reader)
            for row in reader:
                I_data_acum=np.append(I_data_acum,float(row[2]))
                M_data=np.append(M_data,float('0'+row[14]))
                R_data=np.append(R_data,float('0'+row[11]))
                
            I_data_acum=np.flip(I_data_acum)
            M_data=np.flip(M_data)
            R_data=np.flip(R_data)
    else:
        with open('DataConfirmados.csv') as csvfile:
            reader = csv.reader(csvfile)
            I_data_acum,M_data,R_data=0,0,0
            for row in reader:
                if Pais in row:
                    I_data_acum+=np.array([float(i) for i in row[5:]])
        with open('DataMuertos.csv') as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                if Pais in row:
                    M_data+=np.array([float(i) for i in row[5:]])
        with open('DataRecuperados.csv') as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                if Pais in row:
                    R_data+=np.array([float(i) for i in row[5:]])
        i0=min(len(I_data_acum),len(M_data),len(R_data))
        I0=range(i0)
        I_data_acum=I_data_acum[I0]
        R_data=R_data[I0]
        M_data=M_data[I0]


        #Extraemos datos desde el comienzo de la epidemia
    I_data=I_data_acum-(M_data+R_data)
    S_data=Poblacion-I_data_acum #S=Poblacion-Infectados Acumulados
    Ind=I_data_acum>0
    k=sum(Ind)
    #Data=[S,I,R,M,Iacum]
    Data=np.zeros([k,5])
    Data[:,0]=S_data[Ind]
    Data[:,1]=I_data[Ind]
    Data[:,2]=R_data[Ind]
    Data[:,3]=M_data[Ind]
    Data[:,4]=I_data_acum[Ind]

    return Data
