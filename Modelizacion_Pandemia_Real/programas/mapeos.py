from datetime import date, timedelta
import pandas as pd
import geopandas
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import make_axes_locatable
import os
from matplotlib import cm
from matplotlib.colors import ListedColormap
import numpy as np


hoy=str(date.today())
semana=str(date.today()-timedelta(days = 7)),hoy



dir_img="/home/fernando/fer/Investigacion/Trabajo_en_curso/COVID-19/Modelizacion_Pandemia_Real/COVID-19-WEB/imagenes/"
dir_amba="/home/fernando/fer/Investigacion/Trabajo_en_curso/COVID-19/Modelizacion_Pandemia_Real/COVID-19-WEB/provincias/amba/imagenes/"
dir_cor="/home/fernando/fer/Investigacion/Trabajo_en_curso/COVID-19/Modelizacion_Pandemia_Real/COVID-19-WEB/provincias/cordoba/imagenes/"
dir_int="/home/fernando/fer/Investigacion/Trabajo_en_curso/COVID-19/Modelizacion_Pandemia_Real/COVID-19-WEB/internacionales/imagenes/"
dir_prov="/home/fernando/fer/Investigacion/Trabajo_en_curso/COVID-19/Modelizacion_Pandemia_Real/COVID-19-WEB/provincias/imagenes/"



from FitSEIR import downloadWorld, downloadARG
#downloadARG() No funciona ahora estya zipeado
downloadWorld()

downloadARG()
############# LEER BASE ##################################
batch_no=1
dfs = []
chunk_size=1000000
for chunk in pd.read_csv('Data/Epidemic/Covid19Casos.csv',chunksize=chunk_size):
    print(batch_no)
    DataC=chunk[chunk.clasificacion_resumen=='Confirmado']
    dfs.append(DataC)
    batch_no+=1
Data = pd.concat(dfs)


#################################################


#######################################################################
#######################################################################
#####################  PAISES #########################################
#######################################################################
#######################################################################
#######################################################################





################################################################
################### MAPAS ######################################
################################################################

from MapaCOVID import *

################################################################
fig,ax=MapaCOVID(Data,Provincia="Todas",fecha=semana,densidad=1e6,tipo='colorpléctico')
ax.axes.xaxis.set_visible(False)
ax.axes.yaxis.set_visible(False)
plt.savefig(dir_img+"ARGENTINA-casosx1M.png")



###################################################################
#########################  Mundo ##################################
from Graficos import EpiGlobal

#dir="/home/fernando/fer/Investigacion/Trabajo_en_curso/COVID-19-Programas/COVID-19-WEB/imagenes/"

paises=["Chile","Uruguay","Paraguay","Brazil","Bolivia",
        "Peru","Ecuador","Colombia","Venezuela","Panama","Honduras",
        "El Salvador", "Guatemala", 
        "Nicaragua","Costa Rica","Cuba","Dominican Republic","Haiti","Mexico",
        "US","Canada","Spain","Portugal","Italy",
        "United Kingdom","France","Germany","Sweden","Denmark","Norway","Serbia",
        "Romania","Switzerland","Hungary","Turkey","Japan","Korea, South",
        "Czechia","Poland","Hungary","Iceland","Croatia","Russia",
        "China","India","Iran","Iraq","Saudi Arabia","Israel","South Africa","Namibia","Botswana",
        "Zimbabwe","Mozambique","Lesotho","Eswatini"]
EpiGlobal()
plt.savefig(dir_int+"Mundial.png")
plt.close()
for pais in paises:
    EpiGlobal(pais)
    plt.savefig(dir_int+pais+".png")
    plt.close()
# =============================================================================
# 
# 
# from MapaCOVID_world import *   
# hoy=str(date.today()-timedelta(days = 1))
# semana=str(date.today()-timedelta(days = 8)),hoy
# 
# fig,ax=MapaCOVID(semana)
# ax.axes.xaxis.set_visible(False)
# ax.axes.yaxis.set_visible(False)
# plt.savefig(dir_img+"MUNDO-casosx1M.png")
# plt.close()
# =============================================================================







#################### AMBA #############################################
from Graficos import EpiArg1

MapaProv=geopandas.read_file("Data/GeoData/AMBA.json")



partidos=MapaProv.nam


for k in range(3):
    fig, ax = plt.subplots(4,3,figsize=(20,30))
    for l in range(k*4,4*(k+1)):
        i=l-4*k
        for j in range(3):
            if partidos[3*l+j][:6]=='Ciudad':
                EpiArg1(ax[i,j],Data,provincia="CABA")
            else:
                    EpiArg1(ax[i,j],Data,provincia="Buenos Aires",dpto=partidos[3*l+j])
    plt.savefig(dir_amba+'amba-'+str(k)+'.png')
    plt.close()
fig, ax = plt.subplots(1,3,figsize=(20,7))
EpiArg1(ax[0],Data,provincia="Buenos Aires",dpto=partidos[36])
plt.savefig(dir_amba+'amba-'+str(3)+'.png')
plt.close()


#################### cordoba#############################################

MapaProv=geopandas.read_file("Data/GeoData/departamento.json")
MapaProv=MapaProv[[h[:2]=='14' for h in MapaProv['in1']]]


dptos=MapaProv.nam
dptos.index=range(len(dptos))


fig, ax = plt.subplots(4,3,figsize=(20,30))
for l in range(4):
    for j in range(3):
        EpiArg1(ax[l,j],Data,provincia="Córdoba",dpto=dptos[3*l+j])
plt.savefig(dir_cor+'Cba1-'+str(k)+'.png')
plt.close()

fig, ax = plt.subplots(4,3,figsize=(20,30))
for l in range(4,8):
    for j in range(3):
        EpiArg1(ax[l-4,j],Data,provincia="Córdoba",dpto=dptos[3*l+j])
plt.savefig(dir_cor+'Cba2-'+str(k)+'.png')
plt.close()
#################################################


#######################  Provincias #############################
#################################################################
from Graficos import EpiArg1
Provincias=['Buenos Aires','CABA','Catamarca','Chaco','Chubut','Córdoba',
            'Corrientes','Entre Ríos','Formosa','Jujuy','La Pampa',
            'La Rioja','Mendoza','Misiones','Neuquén','Río Negro',
            'Salta','San Juan','Santa Cruz','Santa Fe',
            'Santiago del Estero','Tierra del Fuego','Tucumán'] 

for prov in Provincias:
    fig, ax = plt.subplots(figsize=(8,8))
    EpiArg1(ax,Data,provincia=prov)
    ax.set_title(prov+": "+ hoy,fontsize=18)
    plt.savefig(dir_prov+prov+".png")
    plt.close()
    
    
from Graficos import Sint_Asint,Sint_Asint_edad,PlotEdad

%matplotlib qt

fig, axs = plt.subplots(1,2,figsize=(16,10))
Sint_Asint(axs,Data,provincia='Córdoba',fecha=('2020-04-01',hoy))
plt.savefig(dir_cor+"sint_asint.png")
plt.close()
#Sint_Asint_edad(provincia='Córdoba',fecha=('2020-04-01',hoy))
fig1, ax1 = plt.subplots(1,1,figsize=(20,10))
PlotEdad(ax1,Data,provincia='Córdoba',fecha=('2022-04-01',hoy))
plt.savefig(dir_cor+"Edades.png")
plt.close()



fig4, ax4 = plt.subplots(1,1,figsize=(10,10))
EpiArg1(ax4,Data,provincia="Córdoba")
ax4.set_title("Córdoba: "+ hoy,fontsize=18)
plt.savefig(dir_cor+"Estadistica-General.png")
plt.close()

fig5, ax5 = plt.subplots(1,1,figsize=(10,10))
EpiArg1(ax5,Data,provincia="Argentina")
ax5.set_title("Argentina: "+ hoy,fontsize=18)
plt.savefig(dir_img+"ARGENTINA-General.png")
plt.close()

########################################################
############### FITEOS #################################
########################################################

from FitSEIR import *


dir_fiteo_prov="/home/fernando/fer/Investigacion/Trabajo_en_curso/COVID-19/Modelizacion_Pandemia_Real/COVID-19-WEB/fiteos/imagenes/"



R0_fijo=(1.25,3.02,1.6, .71)
R0_lim=((.5,1.),(1.,2.))
t_lim_fijo=('2021-12-05','2022-01-03','2022-01-20','2022-02-26' )
t_lim=(('2022-04-05','2022-04-25'),)
Rango_I0=((.001,.1),)



FitSEIR(Pais='Argentina',Data=Data,Provincia="Córdoba",
        fecha=('2021-10-01',hoy),
        R0_lim=R0_lim,
        t_lim=t_lim,
        t_lim_fijo=t_lim_fijo,
        R0_fijo=R0_fijo,
        #Metodo='dual_annealing',
        Metodo='dif_ev',
        Rango_I0=Rango_I0,
        p=10,
        save=dir_fiteo_prov)
    


dir_fiteo_dpto="/home/fernando/fer/Investigacion/Trabajo_en_curso/COVID-19/Modelizacion_Pandemia_Real/COVID-19-WEB/fiteos/cordoba/imagenes/"


t_lim_fijo=('2021-12-04','2022-01-05','2022-01-26','2022-02-25')
R0_fijo=(1.02,3.27,1.35,.75)

t_lim=(('2022-04-05','2022-04-25'),)
R0_lim=((.5,1.),(1,2.))


Rango_I0=((.001,.1),)

from FitSEIR import *


FitSEIR(Pais='Argentina',Data=Data,Provincia="Córdoba",dpto='Río Cuarto',
        fecha=('2021-10-01',hoy),
        R0_lim=R0_lim,
        t_lim=t_lim,
        t_lim_fijo=t_lim_fijo,
        R0_fijo=R0_fijo,
        #Metodo='dual_annealing',
        Metodo='dif_ev',
        Rango_I0=Rango_I0,
        save=dir_fiteo_dpto)
    



t_lim_fijo=('2021-12-13', '2022-01-06', '2022-01-26','2022-02-25' )
R0_fijo=(1.22,3.09,1.41,.5)
t_lim=(('2022-04-05','2022-04-25'),)
R0_lim=((.5,1.),(1.,2.))

# t_lim_fijo=()
# t_lim=(('2021-12-05','2021-12-15'),)
# R0_fijo=()
# R0_lim=((1.0,2.0),(1.,4.))
Rango_I0=((.001,.1),)

 
    
FitSEIR(Pais='Argentina',Data=Data,
        fecha=('2021-10-01',hoy),
        R0_lim=R0_lim,
        t_lim=t_lim,
        t_lim_fijo=t_lim_fijo,
        R0_fijo=R0_fijo,
        #Metodo='dual_annealing',
        Metodo='dif_ev',
        Rango_I0=Rango_I0,
        save=dir_fiteo_prov)

                  

# ############# LEER BASE VIEJA ##################################
# batch_no=1
# dfs = []
# chunk_size=1000000

# lenArg=0
# lenCor=0
# lenRio=0
   
# for chunk in pd.read_csv('Data/Epidemic/Covid19Casos_viejo.csv',chunksize=chunk_size):
#     print(batch_no)
#     DataC=chunk[chunk.clasificacion_resumen=='Confirmado']
    
    
    
#     lenArg+=len(DataC)
#     lenCor+=len(DataC[DataC.residencia_provincia_nombre=='Córdoba'])
#     lenRio+=len(DataC[DataC.residencia_departamento_nombre=='Río Cuarto'])
#     batch_no+=1
    


# ##############  Casos nuevos ########################
# print('Casos Nuevos Argentina:' +str(len(Data)-lenArg))

# A=len(Data[Data.residencia_provincia_nombre=='Córdoba'])


# print('Casos Nuevos Córdoba:' +str(A-lenCor))

# A=len(Data[Data.residencia_departamento_nombre=='Río Cuarto'])

# print('Casos Nuevos Río Cuarto:' +str(A-lenRio))



##############  Lo Subimos a Git Hub ########################

import git
repo = git.Repo('/home/fernando/fer/Investigacion/Trabajo_en_curso/COVID-19/Modelizacion_Pandemia_Real/COVID-19-WEB')

repo.git.add(u=True)

repo.index.commit('Datos correspondientes a: '+hoy)

print(repo.remotes.origin.push())



