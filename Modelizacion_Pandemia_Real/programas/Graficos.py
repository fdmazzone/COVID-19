#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sun Jul  5 23:40:51 2020

@author: fernando
"""


########### Ejemplo 1, Grafico area de casos diarios y muertes###############

def EpiArg1(ax1,Data,provincia='Argentina', dpto=None):
    if not provincia=="Argentina":
        Data=Data[Data.residencia_provincia_nombre==provincia]
    if not dpto==None:
        Data=Data[Data.residencia_departamento_nombre==dpto]
    DataM=Data[Data.fallecido=='SI']
    
    J0=Data[['id_evento_caso','fecha_apertura']].groupby('fecha_apertura')
    J1=J0.count().rename(columns={'id_evento_caso':'confirmado_diario'})
    H0=DataM[['id_evento_caso','fecha_fallecimiento']].groupby('fecha_fallecimiento')
    H1=H0.count().rename(columns={'id_evento_caso':'muertes_diarias'})
    H1.index=pd.to_datetime(H1.index)
    J1.index=pd.to_datetime(J1.index)
    
    H2=H1.cumsum().rename(columns={'muertes_diarias':'muertes_acumuladas'})
    J2=J1.cumsum().rename(columns={'confirmado_diario':'confirmados'})
    
    #fig, ((ax1,ax2,ax3),(ax4,ax5,ax6)) = plt.subplots(2,3,figsize=(18,12))
    #fig, ax1 = plt.subplots(figsize=(18,18))
    ax1.set_yscale('log')
    
    J2.plot(ax=ax1,legend=True)
    J1.plot(ax=ax1,legend=True)
    H2.plot(ax=ax1,legend=True)
    H1.plot(ax=ax1,legend=True)
    if dpto==None:
        ax1.set_title(provincia,fontsize=18)
    else:
        ax1.set_title("Departamento "+dpto,fontsize=18)
    ax1.set_xlabel('')




def EpiArgUTI(ax1,Data,provincia='Argentina', dpto=None):
    if not provincia=="Argentina":
        Data=Data[Data.residencia_provincia_nombre==provincia]
    if not dpto==None:
        Data=Data[Data.residencia_departamento_nombre==dpto]
    DataM=Data[Data.fallecido=='SI']
    DataUTI=Data[Data.cuidado_intensivo=='SI']
    DataResp=Data[Data.asistencia_respiratoria_mecanica=='SI']
    
    
    
    J0=Data[['id_evento_caso','fecha_apertura']].groupby('fecha_apertura')
    J1=J0.count().rename(columns={'id_evento_caso':'confirmado_diario'})
    J1.index=pd.to_datetime(J1.index)
    H0=DataM[['id_evento_caso','fecha_apertura']].groupby('fecha_apertura')
    H1=H0.count().rename(columns={'id_evento_caso':'muertes_diarias'})
    H1.index=pd.to_datetime(H1.index)
    K0=DataUTI[['id_evento_caso','fecha_apertura']].groupby('fecha_apertura')
    K1=K0.count().rename(columns={'id_evento_caso':'internaciones'})
    K1.index=pd.to_datetime(K1.index)
    L0=DataResp[['id_evento_caso','fecha_apertura']].groupby('fecha_apertura')
    L1=L0.count().rename(columns={'id_evento_caso':'Respirador'})
    L1.index=pd.to_datetime(L1.index)  
    
    
    #H2=H1.cumsum().rename(columns={'muertes_diarias':'muertes_acumuladas'})
    #J2=J1.cumsum().rename(columns={'confirmado_diario':'confirmados'})
    
    #fig, ((ax1,ax2,ax3),(ax4,ax5,ax6)) = plt.subplots(2,3,figsize=(18,12))
    #fig, ax1 = plt.subplots(figsize=(18,18))
    ax1.set_yscale('log')
    
    #J2.plot(ax=ax1,legend=True)
    J1.plot(ax=ax1,legend=True)
    #H2.plot(ax=ax1,legend=True)
    H1.plot(ax=ax1,legend=True)
    K1.plot(ax=ax1,legend=True)
    L1.plot(ax=ax1,legend=True)
    
    if dpto==None:
        ax1.set_title("Casos, muertes, internaciones, asistencia respiratoria:"+provincia,fontsize=18)
    else:
        ax1.set_title("Casos, muertes, internaciones, asistencia respieratoria: "+dpto,fontsize=18)
    ax1.set_xlabel('')





def EpiArg(Data,provincia='Todas', dpto=None):
    if not provincia=="Todas":
        Data=Data[Data.residencia_provincia_nombre==provincia]
    if not dpto==None:
        Data=Data[Data.residencia_departamento_nombre==dpto]
    DataM=Data[Data.fallecido=='SI']
    
    J0=Data[['id_evento_caso','fecha_apertura']].groupby('fecha_apertura')
    J1=J0.count().rename(columns={'id_evento_caso':'confirmado_diario'})
    H0=DataM[['id_evento_caso','fecha_fallecimiento']].groupby('fecha_fallecimiento')
    H1=H0.count().rename(columns={'id_evento_caso':'muertes_diarias'})
    H1.index=pd.to_datetime(H1.index)
    J1.index=pd.to_datetime(J1.index)
    
    H2=H1.cumsum().rename(columns={'muertes_diarias':'muertes_acumuladas'})
    J2=J1.cumsum().rename(columns={'confirmado_diario':'confirmados'})
    
    
    HJ=DataM.groupby('fecha_apertura').count().id_evento_caso
    HJ.index=pd.to_datetime(HJ.index)
    I=J1.index.difference(HJ.index)
    
    
    HH=pd.Series(np.zeros(len(I)), index=I).sort_index()
    HL=pd.concat([HJ,HH])
    MuertesTasa=(100*HL.divide(J1.confirmado_diario)).rename('tasa_muertes')
    

    J3=Data.groupby('edad').edad.count()
    H3=DataM.groupby('edad').edad.count()
    
    
    
    HH=pd.Series(np.zeros(len(I)), index=I).sort_index()
    HL=pd.concat([HJ,HH])
    MuertesTasa=(100*HL.divide(J1.confirmado_diario)).rename('tasa_muertes')
    
    
    #fig, ((ax1,ax2,ax3),(ax4,ax5,ax6)) = plt.subplots(2,3,figsize=(18,12))
    fig, ((ax1,ax2),(ax3,ax4)) = plt.subplots(2,2,figsize=(18,18))
    ax1.set_yscale('log')
    
    J2.plot(ax=ax1,legend=True)
    J1.plot(ax=ax1,legend=True)
    H2.plot(ax=ax1,legend=True)
    H1.plot(ax=ax1,legend=True)
    if dpto==None:
        ax1.set_title(provincia,fontsize=18)
    else:
        ax1.set_title("Departamento "+dpto,fontsize=18)
    ax1.set_xlabel('')

    ############# Ejemplo 2 Histogramas edades
    DataM.hist('edad',ax=ax2,bins=np.arange(0,100,2))
    ax2.set_title(u"Distribución edad muertes",fontsize=18)
    #########3###Ejemplo 3, diagrama torta de sexos
    DataM.sexo.value_counts().plot.pie(ax=ax3)
    ax3.set_title(u"Distribución muertes por sexo",fontsize=18)
    

    
    ############# Ejemplo 6 Histogramas edades infectados
    H4=(H3.divide(J3)*100)
    H4[~H4.isnull()].plot.bar(ax=ax4)
    ax4.set_title(u"Letalidad por Edad (%)",fontsize=18)
    
    
    
    fig1, ax5 = plt.subplots(figsize=(8,8))
        #############  Ejemplo 4, Analisis de edad media muertes
    
#    DataM_g=DataM.groupby('fecha_fallecimiento').mean()
#    DataM_g.edad.plot(ax=ax4)
#    DataM_g.edad.rolling(20, center=True).mean().plot(ax=ax4)
#    ax4.set_title(u"Evolución edad media muertes",fontsize=18)
    
#    #####   Ejemplo 5. Tasa mortalidad vs tiempo
    MuertesTasa.rolling(20, center=True).mean().plot(ax=ax5)
    ax5.set_title(u"Tasa letalidad",fontsize=18)
########## Ejemplo 5. Grafico area confirmados, 
### confirmados diarios y muertes globales

def EpiGlobal(Pais='Estadística Mundial'):
    DataC, DataM, DataR=readData(Pais)
    fecha=str(DataC.index[-1])[:10]
    DataCd=DataC.diff().apply(abs).rename('Confirmados diarios')
    fig,ax=plt.subplots(figsize=(8,8))
    plt.yscale('log')
    print(min(DataC))
    DataC.plot(ax=ax,legend=True)
    DataCd.plot(ax=ax,legend=True)
    DataM.plot(ax=ax,legend=True)
    DataM.diff().apply(abs).rename('muertes_diarias').plot(ax=ax,legend=True)
    ax.set_title(Pais+'('+fecha+')',fontsize=18)
    
def Sint_Asint(axs,Data,provincia='Todas',dpto=None,fecha=None):
       
    Data=readDataArg(Data,provincia=provincia,dpto=dpto)
    if not fecha==None:
        I1=Data.fecha_apertura>=fecha[0]
        I2=Data.fecha_apertura<=fecha[1]
        Data=Data[I1 & I2]
    
    DataSint=Data[Data.fecha_inicio_sintomas.notnull()]
    DataInt=DataSint[DataSint.cuidado_intensivo=='SI']
    
    
    J0=Data[['id_evento_caso','fecha_apertura']].groupby('fecha_apertura')
    J1=J0.count().rename(columns={'id_evento_caso':'casos_acumulados'})
    H0=DataSint[['id_evento_caso','fecha_apertura']].groupby('fecha_apertura')
    H1=H0.count().rename(columns={'id_evento_caso':'casos_sintomaticos_acumulados'})
    K0=DataInt[['id_evento_caso','fecha_apertura']].groupby('fecha_apertura')
    K1=K0.count().rename(columns={'id_evento_caso':'cuidado_intensivo_acumulados'})

    H1.index=pd.to_datetime(H1.index)
    J1.index=pd.to_datetime(J1.index)
    K1.index=pd.to_datetime(K1.index)

    
    H2=H1.cumsum()#.rename(columns={'casos_sintomáticos_acumulados':'casos_asint_acumuladas'})
    J2=J1.cumsum()#.rename(columns={'casos_diarios':'casos_acumulados'})
    K2=K1.cumsum()
    
    #fig, (ax1,ax2) = plt.subplots(1,2,figsize=(16,10))
    ax1,ax2=axs
    ax1.set_yscale('log')
    J2.plot(ax=ax1,Marker='o',legend=True)
    H2.plot(ax=ax1,Marker='o',legend=True)
    K2.plot(ax=ax1,Marker='o',legend=True)
    ax1.set_title(provincia+': Confirmados, Sintomáticos, Cuidado Intensivo',fontsize=18)

    I=J2.index.difference(H2.index)
    nan_array=np.empty(len(I))
    nan_array[:]=np.NaN
    HH=pd.Series(nan_array, index=I).sort_index()
    H2=pd.concat([H2.casos_sintomaticos_acumulados,HH]).sort_index()
    H3=H2.divide(J2.casos_acumulados)*100
    H3.rename(u'asintomáticos (%)')
    H3.plot(ax=ax2,Marker='o')
    ax2.set_title(provincia+': Relación sintomáticos al total (%)',fontsize=18)
    
    
def Sint_Asint_edad(Data,provincia='Todas',dpto=None,fecha=None):
        
        
        Data=readDataArg(Data,provincia=provincia,dpto=dpto)
        if not fecha==None:
            I1=Data.fecha_apertura>=fecha[0]
            I2=Data.fecha_apertura<=fecha[1]
            Data=Data[I1 & I2]
        
        
        i=0
        marker=[".",",","o","v","^","<",">","1","2","3","4","8","s","p","P"]
    
        rangos=[(10*i,10*(i+1)) for i in range(1,8)]
        
        
        fig, ax = plt.subplots(figsize=(16,10))
        ax.set_title(u'Relación sintomáticos al total',fontsize=18)

        
        
        for edad in rangos:
            I=(Data.edad>=edad[0]) & (Data.edad<edad[1])
            DataEdad=Data[I]
            
            DataSint=DataEdad[DataEdad.fecha_inicio_sintomas.notnull()]
            
            
            J0=DataEdad[['id_evento_caso','fecha_apertura']].groupby('fecha_apertura')
            J1=J0.count().rename(columns={'id_evento_caso':'casos_acumulados'})
            H0=DataSint[['id_evento_caso','fecha_apertura']].groupby('fecha_apertura')
            H1=H0.count().rename(columns={'id_evento_caso':'casos_sintomaticos_acumulados'})
            
            H1.index=pd.to_datetime(H1.index)
            J1.index=pd.to_datetime(J1.index)
        
        
            
            H2=H1.cumsum()#.rename(columns={'casos_sintomáticos_acumulados':'casos_asint_acumuladas'})
            J2=J1.cumsum()#.rename(columns={'casos_diarios':'casos_acumulados'})
        
            
        
        
            I=J2.index.difference(H2.index)
            nan_array=np.empty(len(I))
            nan_array[:]=np.NaN
            HH=pd.Series(nan_array, index=I).sort_index()
            H2=pd.concat([H2.casos_sintomaticos_acumulados,HH]).sort_index()
            H3=H2.divide(J2.casos_acumulados)*100
            #H3.rename(u'asintomáticos (%)')
            H3=H3.to_frame().rename(columns={0:str(edad)})
            H3.plot(ax=ax,Marker=marker[i],legend=True)
            i=i+1
    
  


def PlotEdad(ax,Data,provincia='Todas',dpto=None,fecha=None):
    Data=readDataArg(Data,provincia=provincia,dpto=dpto)
    if not fecha==None:
        I1=Data.fecha_apertura>=fecha[0]
        I2=Data.fecha_apertura<=fecha[1]
        Data=Data[I1 & I2]
    rangos=[(i*5,(i+1)*5) for i in range(1,16)]
    #Para CABA 
    #Hab=[165638, 156372, 150501, 167681, 228125, 247594, 248069,
    #     215326, 180876, 171626, 171021,161136,152115,128415 ,105173,
    #     93296]
    #Hab=[261668,266477,277367,283495,274482,260568,254546,
         #216835,188392,184201,169053,158229,144045,116607,92476,72476]
    
    HabCor=[295849,273321,277825,294468,301944,282113,263742,
            256613,219638,189946,179599,161529,144170,122309,89838]
    
    Hab=HabCor
    
    
    #rangos=((0,30),(30,45),(46,60),(60,np.Inf))
    #fig, ax = plt.subplots(1,1,figsize=(10,10))
    ax.set_title(provincia+ ": Casos cada 100.000 por grupos etarios (smoothing)",fontsize=26)
    JT0=Data[['id_evento_caso','fecha_apertura']].groupby('fecha_apertura')
    JT=JT0.count().rename(columns={'id_evento_caso':'confirmado_diario'})
    #ax.set_yscale('log')
    i=0
    marker=[".",",","o","v","^","<",">","1","2","3","4","8","s","p","P"]
    for edad in rangos:
        I=(Data.edad>=edad[0]) & (Data.edad<edad[1])
        DataEdad=Data[I]
        J0=DataEdad[['id_evento_caso','fecha_apertura']].groupby('fecha_apertura')
        J1=J0.count().rename(columns={'id_evento_caso':str(edad)})
        #J2=J1[str(edad)]/JT['confirmado_diario']*100 
        J2=J1[str(edad)]/Hab[i]*1e5
        J2=J2.to_frame().rename(columns={0:str(edad)})
        J2.index=pd.to_datetime(J2.index)
        #J2=J1.cumsum()
        #J2.plot(ax=ax,marker=marker[i],legend=True)
        J2.rolling(20, center=True).mean().plot(ax=ax,marker=marker[i],markersize=10,legend=True)
        #J2.plot(ax=ax,marker=marker[i],legend=True)
        i=i+1


#################  Rvisar la funcion siguiente, no funciona
def PlotDifFechas(Data,provincia='Todas',dpto=None):
    Data=readDataArg(Data,provincia=provincia,dpto=dpto)
    fig, ax = plt.subplots(1,1,figsize=(10,10))
    J0=Data[['fecha_apertura','fecha_diagnostico']]
    J0['diferencia']=pd.to_datetime(J0['fecha_apertura'])-pd.to_datetime(J0['fecha_diagnostico']) 
    J1=J0.sort_values(by='fecha_apertura',axis=0)
    S1=J1.groupby('fecha_apertura').sum().diferencia
    S2=J1.groupby('fecha_apertura').count().diferencia
    Ratio=(S1/S2)/24.0/3600.0/1.0e9/np.timedelta64(1,'ns')
    Ratio.plot(ax=ax,Marker='o')

#################  Rvisar la funcion siguiente, hay que usar la base total
def Testeos(axs,provincia='Argentina', dpto=None):
    batch_no=1
    dfs = []
    chunk_size=1000000
    for chunk in pd.read_csv('Data/Epidemic/Covid19Casos.csv',chunksize=chunk_size):
        print(batch_no)
        if not provincia=="Argentina":
            A=chunk[chunk.residencia_provincia_nombre==provincia]
        else:
            A=chunk
        if not dpto==None:
            A=chunk[chunk.residencia_departamento_nombre==dpto]
        B=A[['fecha_apertura','clasificacion_resumen','fallecido','id_evento_caso','fecha_apertura']]
        dfs.append(B)
        batch_no+=1
    L0 = pd.concat(dfs).groupby('fecha_apertura')
    

    
    DataC=L0[L0.clasificacion_resumen=='Confirmado']
    DataM=DataC[DataC.fallecido=='SI']
    
    J0=DataC[['id_evento_caso','fecha_apertura']].groupby('fecha_apertura')
    J1=J0.count().rename(columns={'id_evento_caso':'confirmado_diario'})
    #H0=DataM[['id_evento_caso','fecha_fallecimiento']].groupby('fecha_fallecimiento')
    #H1=H0.count().rename(columns={'id_evento_caso':'muertes_diarias'})
    #H1.index=pd.to_datetime(H1.index)
    J1.index=pd.to_datetime(J1.index)
    
    #H2=H1.cumsum().rename(columns={'muertes_diarias':'muertes_acumuladas'})
    J2=J1.cumsum().rename(columns={'confirmado_diario':'confirmados'})
    
    
    

    

    
    
    
    #L0=Data[['id_evento_caso','fecha_apertura']].groupby('fecha_apertura')
    
    L1=L0.count().rename(columns={'id_evento_caso':'evento_diario'}) 
    L1.index=pd.to_datetime(L1.index)
    
    L2=L1.cumsum().rename(columns={'evento_diario':'evento_acumulado'}) 
    
    #fig, (ax1,ax2) = plt.subplots(2,1,figsize=(18,12))
    ax1,ax2=axs
    ax1.set_yscale('log')
    ax1.set_title(provincia+": Casos diarios y testeos",fontsize=26)
    ax2.set_title(provincia+": Relación casos diarios a testeos (%)",fontsize=26)
    J2.plot(ax=ax1,Marker='+',legend=True)
    J1.plot(ax=ax1,Marker='^',legend=True)
    #H2.plot(ax=ax1,legend=True)
    #H1.plot(ax=ax1,legend=True)
    
    #fig2, ax2= plt.subplots(1,1,figsize=(18,12))
    #ax2.set_yscale('log')
    L2.plot(ax=ax1,Marker='p',legend=True)
    L1.plot(ax=ax1,Marker='o',legend=True)


    #fig2, ax2 = plt.subplots(1,1,figsize=(18,12))
    
    Razon=J1.confirmado_diario/L1.evento_diario*100
    Razon.plot(ax=ax2)
    
def MapaCOVID(provincia):
    """
        Hace un mapa de la provincia dividida por departamentos y colorea con 
        intensidades acorde a la cantidad de infectados totales de cada 
        departamento. 
    """
    

    
    
    if provincia=="AMBA":
        filepath4=dir1+"/Data/GeoData/AMBA.json"
        MapaProv=geopandas.read_file(filepath4)
        MapaProv.insert(9, "MuertesxInfectado", 0.0)
        MapaProv.index=MapaProv.in1
        DataProv=readDataArg(Data,provincia='AMBA')       
    else:
        Arg=geopandas.read_file(filepath2)
        CodProv=str(codigo.Cod[provincia]).zfill(2)
        MapaProv=Arg[[h[:2]==CodProv for h in Arg['in1']]]
        MapaProv.insert(9, "MuertesxInfectado", 0.0)#isertar columna nueva
        MapaProv.index=MapaProv.in1
        DataProv=readDataArg(Data,provincia=provincia)
        
    if len(DataProv)==0:
        return "No se registra"
    if provincia=="AMBA":
        CasosCABA=DataProv[DataProv.residencia_provincia_nombre=='CABA']
        Total=float(len(CasosCABA))
        H=CasosCABA.fallecido.value_counts()
        MapaProv.at['02',"MuertesxInfectado"]=float(H['SI'])/Total*100
        
        
        
        
        DataProv=DataProv[DataProv.residencia_provincia_id==6]
        DataProvM=DataProv[DataProv.fallecido=='SI']
        
        
        DataI=DataProv.residencia_departamento_id.value_counts()
        
        DataIM=DataProvM.residencia_departamento_id.value_counts()

        
        for h in DataIM.index:
            #if not(h==0):
            id='06'+str(h).zfill(3)
            MapaProv.at[id,"MuertesxInfectado"]=float(DataIM[h])/float(DataI[h])*100
    else:
        DataI=DataProv.residencia_departamento_id.value_counts()
        DataProvM=DataProv[DataProv.fallecido=='SI']
        DataIM=DataProvM.residencia_departamento_id.value_counts()
        for h in DataIM.index:
            #if not(h==0):
            id=CodProv+str(h).zfill(3)
            print(id)
            MapaProv.at[id,"MuertesxInfectado"]=float(DataIM[h])/float(DataI[h])*100
        
    fig, ax = plt.subplots(1, 1)
    divider = make_axes_locatable(ax)
    cax = divider.append_axes("right", size="5%", pad=0.1)
    MapaProv.plot(column='MuertesxInfectado',ax=ax,cax=cax,edgecolor="black",cmap=newcmp , legend=True)  
    ax.set_title(provincia,fontsize=26)
    
    fig1, ax1 = plt.subplots(1, 1)
    
    Resultado=MapaProv.sort_values("MuertesxInfectado",ascending=False)
    Resultado.MuertesxInfectado.plot.bar(ax=ax1)
    return Resultado.nam

def readDataArg(Data,provincia='Todas', dpto=None,filtro='Confirmado'):
    if not provincia=="Todas":
        if provincia=='AMBA':
            DataAMBA=geopandas.read_file(dir1+'/Data/GeoData/AMBA.json')
            #Primer datos es CABA lo leere de otra forma
            I1=[int(i[2:]) for i in DataAMBA.in1.values[1:]]
            I2=Data['residencia_provincia_id']==6
            I3=Data['residencia_departamento_id'].isin(I1)
            I4=Data['residencia_provincia_id']==2
            I= (I3 & I2) | I4 
    
            Data=Data.loc[I]
        else:
            Data=Data[Data.residencia_provincia_nombre==provincia]
            if not dpto==None:
                Data=Data[Data.residencia_departamento_nombre==dpto]
    return Data
######################  Paises ################################################
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
    
    if not Pais=="Estadística Mundial":
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
import os
from matplotlib import cm
from matplotlib.colors import ListedColormap
import numpy as np



#############  Nueva COLOR MAP ###############33
viridis = cm.get_cmap('Greens', 4096)
newcolors = viridis(np.linspace(0, 1, 4096))
white = np.array([.0, .0, .0, .0])
newcolors[:1, :] = white
newcmp = ListedColormap(newcolors)

##################  DIRECCIONES DE CARPETAS ###################################
dir1=os.getcwd()
filepath1=dir1+"/Data/Epidemic/Covid19Casos.csv"
filepath2=dir1+"/Data/GeoData/departamento.json"
filepath3=dir1+"/Data/GeoData/provincia.json"


######################  CODIGOS DE provincia ##################################
codigo=pd.read_csv(dir1+'/Data/GeoData/CodProv.csv')
codigo.index=codigo.Provincia








