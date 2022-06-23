################# FITEOS #########################
#################################################
from FitSEIR import *
from datetime import date, timedelta

hoy=str(date.today())
semana=str(date.today()-timedelta(days = 7)),hoy

from FitSEIR import downloadARG, downloadWorld
#downloadARG() No funciona ahora estya zipeado
downloadWorld()




#################################################

dir="/home/fernando/fer/Investigacion/Trabajo_en_curso/COVID-19-Programas/COVID-19-WEB/"
dir_img=dir+ "imagenes/"
dir_prov=dir+"provincias/"
dir_prov_imag=dir_prov+"imagenes/"
dir_prov_amba=dir_prov+"amba/imagenes/"
dir_prov_cordoba=dir_prov+"cordoba/imagenes/"
dir_int=dir+"internacionales/imagenes/"
dir_fiteo=dir+"fiteos/"
dir_cor=dir_fiteo+"cordoba/imagenes/"
dir_fiteo_prov=dir_fiteo+"imagenes/"

#################################################
###########      Argentina    ###################
#################################################
t_lim_fijo=('2020-03-30','2020-05-02','2020-07-04','2020-10-18',
            '2020-12-14','2021-01-12')
t_lim=(('2021-02-05','2021-02-20'),)
R0_fijo=(3.41,1.05,1.44,1.14,.86,1.29)
R0_lim=((.8,.95),(.5,1.5))
Rango_I0=((.9,1),)
FitSEIR(Pais='Argentina',fecha=('2020-03-01','2021-05-30'),
    R0_lim=R0_lim,R0_fijo=R0_fijo,t_lim=t_lim,
    t_lim_fijo=t_lim_fijo,
    Rango_I0=Rango_I0,save=dir_fiteo_prov)#,Metodo='dual_annealing')

#################################################
###########     Buenos Aires  ###################
#################################################
t_lim_fijo=('2020-03-19','2020-04-14','2020-08-01','2020-10-13','2020-12-08' ,'2021-01-08')
t_lim=()
R0_fijo=(3.96,1.25,1.39,1.01,.87,1.35)
R0_lim=((.8,1.),)
dir=dir_fiteo+"imagenes/"
Rango_I0=((.9,.95),)
FitSEIR(Provincia='Buenos Aires',fecha=('2020-03-01',hoy),R0_lim=R0_lim,
    R0_fijo=R0_fijo,t_lim=t_lim,t_lim_fijo=t_lim_fijo,
    Rango_I0=Rango_I0,p=2.0,save=dir_fiteo_prov)#,Metodo='dual_annealing')

#################################################
###########     La Matanza  ###################
#################################################
t_lim_fijo=('2020-07-30','2020-10-10','2020-12-11','2021-01-08')
t_lim=()
R0_fijo=(1.36,.98,.8,1.49)
R0_lim=((.7,1.),)
Rango_I0=((.9,.95),)
FitSEIR(Provincia='Buenos Aires',dpto='La Matanza', fecha=('2020-04-15',hoy),R0_lim=R0_lim,
        R0_fijo=R0_fijo,t_lim=t_lim,t_lim_fijo=t_lim_fijo,
        Rango_I0=Rango_I0,p=2.0,save=dir_fiteo+"/amba/imagenes")#,Metodo='dual_annealing')


#################################################
###########     CABA    ###################
##################################################
t_lim_fijo=('2020-03-19','2020-04-13','2020-06-15','2020-09-05', 
            '2020-11-05','2020-12-14','2021-01-11')
t_lim=()
R0_fijo=(3.96,1.01,1.49,1.09,.88,1.06,1.41)
R0_lim=((.5,1.5),)
FitSEIR(Provincia='CABA',fecha=('2020-03-01',hoy),R0_lim=R0_lim,
    R0_fijo=R0_fijo,t_lim=t_lim,t_lim_fijo=t_lim_fijo,save=dir_fiteo+"imagenes/")#,Metodo='dual_annealing')




#################################################
###########      Córdoba      ###################
#################################################


t_lim_fijo=('2020-06-06','2020-08-01','2020-10-11',
            '2020-11-15','2020-12-17','2021-01-17')
t_lim=()
R0_lim=((0.6,.9),)
R0_fijo=(.89,1.48,1.38,.94,.73,1.2)
FitSEIR(Provincia='Córdoba',fecha=('2020-04-01',hoy),R0_lim=R0_lim,
    R0_fijo=R0_fijo,t_lim=t_lim,t_lim_fijo=t_lim_fijo,
    Rango_I0=((.66,.68),),save=dir_fiteo+"imagenes/")#Metodo='dual_annealing')






#################################################
###########    CALAMUCHITA    ###################
#################################################
t_lim_fijo=('2020-10-09','2020-12-05' )
t_lim=()
R0_lim=((.5,1.7),)
R0_fijo=(1.47,.6)

FitSEIR(Provincia='Córdoba',dpto='Calamuchita',fecha=('2020-08-01',hoy),
           R0_lim=R0_lim,R0_fijo=R0_fijo,t_lim=t_lim,
           t_lim_fijo=t_lim_fijo,
           Rango_I0=((.8,.9),),save=dir_cor)#,Metodo='dual_annealing')

#################################################
###########     Capital    ###################
#################################################

t_lim_fijo=('2020-10-10','2020-11-10','2020-12-18','2021-01-14')
t_lim=()
R0_lim=((.5,1.),)
R0_fijo=(1.42,.98,.7,1.26)
FitSEIR(Provincia='Córdoba',dpto='Capital',fecha=('2020-07-01',hoy),
        R0_lim=R0_lim,R0_fijo=R0_fijo,t_lim=t_lim,t_lim_fijo=t_lim_fijo,
        Rango_I0=((.1,.2),),save=dir_cor)#,Metodo='dual_annealing')



#################################################
###########    GENERAL SAN MARTIN    ###################
#################################################

t_lim_fijo=('2020-10-12','2020-12-30')
t_lim=()
R0_lim=((.5,1.5),)
R0_fijo=(1.45,.83)

FitSEIR(Provincia='Córdoba',dpto='General San Martín',fecha=('2020-07-01',hoy),
           R0_lim=R0_lim,R0_fijo=R0_fijo,t_lim=t_lim,t_lim_fijo=t_lim_fijo,
           Rango_I0=((.1,.2),),save=dir_cor)#,Metodo='dual_annealing')


#################################################
###########    General Roca    ###################
#################################################

t_lim_fijo=()
t_lim=(('2020-09-27','2020-10-05'),)
R0_lim=((1.3,1.7),(1.0,1.5))
R0_fijo=()

FitSEIR(Provincia='Córdoba',dpto='General Roca',fecha=('2020-09-01',hoy),
           R0_lim=R0_lim,R0_fijo=R0_fijo,t_lim=t_lim,t_lim_fijo=t_lim_fijo,
           save=dir_cor)#,Metodo='dual_annealing')


 #################################################
###########    Juárez Celman    ###################
#################################################

t_lim_fijo=('2020-09-02','2020-11-07','2020-12-26')
t_lim=()
R0_lim=((1.,1.7),)
R0_fijo=(1.93,1.02,.64)

FitSEIR(Provincia='Córdoba',dpto='Juárez Celman',fecha=('2020-08-01',hoy),
           R0_lim=R0_lim,R0_fijo=R0_fijo,t_lim=t_lim,t_lim_fijo=t_lim_fijo,
           save=dir_cor)#,Metodo='dual_annealing')


 #################################################
###########    Marcos Juárez     ###################
#################################################

t_lim_fijo=('2020-09-12','2020-10-03')
t_lim=()
R0_lim=((.8,.9),)
R0_fijo=(1.0,1.6)

FitSEIR(Provincia='Córdoba',dpto='Marcos Juárez',fecha=('2020-08-01',hoy),
           R0_lim=R0_lim,R0_fijo=R0_fijo,t_lim=t_lim,t_lim_fijo=t_lim_fijo,
           save=dir_cor)#,Metodo='dual_annealing')


#################################################
###########    Presidente Roque Sáenz  Peña  #####
#################################################

t_lim_fijo=('2020-10-26',)
t_lim=()
R0_lim=((.8,1.),)
R0_fijo=(1.27,)

FitSEIR(Provincia='Córdoba',dpto='Presidente Roque Sáenz Peña',
        fecha=('2020-09-17',hoy),
           R0_lim=R0_lim,R0_fijo=R0_fijo,t_lim=t_lim,t_lim_fijo=t_lim_fijo,
           Rango_I0=((.2,.3),),save=dir_cor)#,Metodo='dual_annealing')

#################################################
###########     Río Cuarto    ###################
#################################################

t_lim_fijo=('2020-09-05','2020-10-20','2020-11-14','2020-12-15',
            '2021-01-10')
t_lim=()
R0_lim=((.5,1.3),)
R0_fijo=(1.92,1.04,.89,.58,1.45)

FitSEIR(Provincia='Córdoba',dpto='Río Cuarto',fecha=('2020-08-01',hoy),
           R0_lim=R0_lim,R0_fijo=R0_fijo,t_lim=t_lim,
           Rango_I0=((.8,.81),),t_lim_fijo=t_lim_fijo,save=dir_cor)#,Metodo='dual_annealing')



#################################################
###########    Tercero Arriba    ###################
#################################################

t_lim_fijo=('2020-07-25','2020-09-03','2020-09-28','2020-11-05','2020-12-02' )
t_lim=()
R0_lim=((1.,2.),)
R0_fijo=(3.5,.8,1.88,1.07,.5)

FitSEIR(Provincia='Córdoba',dpto='Tercero Arriba',fecha=('2020-07-14',hoy),
           R0_lim=R0_lim,R0_fijo=R0_fijo,t_lim=t_lim,t_lim_fijo=t_lim_fijo,
           Rango_I0=((.6,.7),),save=dir_cor)#,Metodo='dual_annealing')




#################################################
###########    UNION   ###################
#################################################

t_lim_fijo=('2020-09-29',)
t_lim=()
R0_lim=((0.8,1.0),)
R0_fijo=(2.05,)

FitSEIR(Provincia='Córdoba',dpto='Unión',fecha=('2020-09-17',hoy),
           R0_lim=R0_lim,R0_fijo=R0_fijo,t_lim=t_lim,t_lim_fijo=t_lim_fijo,
           Rango_I0=((.5,.6),),save=dir_cor)#,Metodo='dual_annealing')

#################################################
###########     Jujuy         ###################
#################################################
t_lim_fijo=('2020-07-19','2020-09-06')
t_lim=(('2020-12-05','2020-12-15'),)
R0_fijo=(1.68,1.23)
R0_lim=((.5,.65),(1.1,1.6))

FitSEIR(Provincia='Jujuy',fecha=('2020-06-20',hoy),R0_lim=R0_lim,
    R0_fijo=R0_fijo,t_lim=t_lim,t_lim_fijo=t_lim_fijo,p=2.0,save=dir_fiteo+"imagenes/")
    #,Metodo='dual_annealing')


#################################################
###########     Mendoza       ###################
#################################################

t_lim_fijo=('2020-09-09','2020-11-04')
t_lim=()
R0_lim=((.5,1.),)
R0_fijo=(1.5,1.0)


FitSEIR(Provincia='Mendoza',fecha=('2020-06-12',hoy),
    R0_lim=R0_lim,R0_fijo=R0_fijo,t_lim=t_lim,t_lim_fijo=t_lim_fijo,
    Rango_I0=((.1,.2),),save=dir_fiteo+"imagenes/")#,Metodo='dual_annealing')


#################################################
###########     Santa Fe      ###################
#################################################


t_lim_fijo=()
t_lim=(('2020-10-15','2020-10-25'),)
R0_fijo=()
R0_lim=((1.,1.5),(.5,1.0))
Rango_I0=((.8,.9),)
FitSEIR(Provincia='Santa Fe',fecha=('2020-08-01',hoy),R0_lim=R0_lim,
    R0_fijo=R0_fijo,t_lim=t_lim,
    t_lim_fijo=t_lim_fijo,
    Rango_I0=Rango_I0,save=dir_fiteo+"imagenes/")#,Metodo='dual_annealing')





#################################################
###########     Tucumán       ###################
#################################################

t_lim_fijo=('2020-09-12',)
t_lim=(('2020-10-15','2020-10-25'),)
R0_lim=((1.2,1.3),(0.0,1.0))
R0_fijo=(1.64,)


FitSEIR(Provincia='Tucumán',fecha=('2020-07-20',hoy),
    R0_lim=R0_lim,R0_fijo=R0_fijo,t_lim=t_lim,t_lim_fijo=t_lim_fijo,
    save=dir_fiteo_prov)#,Metodo='dual_annealing')



#################################################
###########     La Pampa       ###################
#################################################

t_lim_fijo=('2020-07-30' , '2020-08-25' , '2020-09-14' , '2020-10-19' , 
            '2020-12-07', '2021-01-03' )
t_lim=()
R0_lim=((.6,.8),)
R0_fijo=(3.99 ,0.27 ,2.19,1.50,1.00,1.49)


FitSEIR(Provincia='La Pampa',fecha=('2020-07-23',hoy),
    R0_lim=R0_lim,R0_fijo=R0_fijo,t_lim=t_lim,t_lim_fijo=t_lim_fijo,
    Rango_I0=((.9,.92),),save=dir_fiteo+"imagenes/")#,Metodo='dual_annealing')

#################################################
###########    Brasil      ###################
#################################################
#################################################
t_lim_fijo=('2020-03-21','2020-04-09','2020-06-03','2020-11-06')
t_lim=()
R0_fijo=(4.0 , 2.59 , 1.54 ,1.0)
R0_lim=((1.0,1.8),)
FitSEIR(Pais='Brazil',fecha=('2020-03-01',hoy),
    R0_lim=R0_lim,R0_fijo=R0_fijo,t_lim=t_lim,
    t_lim_fijo=t_lim_fijo,
    save=dir_fiteo+"imagenes/")#,Metodo='dual_annealing')






"""

#################################################
###########      Cuba    ###################
#################################################
t_lim_fijo=('2020-04-14','2020-09-01','2020-08-17')
t_lim=()
R0_fijo=(2.6,0.75)
R0_lim=((1.75,1.8),(.5,1.0))


FitSEIR(Pais='Cuba',fecha=('2020-03-16',hoy),
    R0_lim=R0_lim,R0_fijo=R0_fijo,t_lim=t_lim,t_lim_fijo=t_lim_fijo)#,Metodo='dual_annealing')

#################################################
###########      Italia    ###################
#################################################
t_lim_fijo=('2020-03-21','2020-04-16','2020-07-06')
t_lim=()
R0_fijo=(2.39,.95,.69)
R0_lim=((1.2,1.5),)

FitSEIR(Pais='Italy',fecha=('2020-03-01',hoydo),
    R0_lim=R0_lim,R0_fijo=R0_fijo,t_lim=t_lim,t_lim_fijo=t_lim_fijo,Metodo='dual_annealing')



#################################################
###########      China    ###################
#################################################
t_lim_fijo=()
t_lim=(('2020-02-10','2020-02-11'),)
R0_fijo=()
R0_lim=((2.9,3.),(0.0,.25))

FitSEIR(Pais='China',fecha=('2020-01-10','2020-03-12'),
    R0_lim=R0_lim,R0_fijo=R0_fijo,t_lim=t_lim,t_lim_fijo=t_lim_fijo,Metodo='dual_annealing')


##############  mapas ####################################33
"""