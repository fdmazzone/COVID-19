#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Fri Jul 17 16:21:00 2020

@author: Fernando Mazzone
"""
def SIR_2C_estocastico(N1,N2,n,R01,R02,media_transf,delta_s):
    """
    Dos ciudades sobre las que avanza una epidemia. En cada una de ellas se
    asume un modelos SIR discreto. Se asume que en cada iteración con 
    probabilidad p un individuo de una ciudad puede pasar a la otra.
    La primera ciudad con un número de reproducción básico R01 y la segunda 
    con R02. La unidad de tiempo es el periodo de infectividad y la población
    total está normalizada N=1.
    Parametros:
        n: int (#iteraciones)
        R01: float64,  número de reproducción básico ciudad 1
        R02: float64,  número de reproducción básico ciudad 2
        p: float64, probabilidad que se intercambie Delta_H habitantes
           entre ciudades
        Delta_H: float 64 algo así como un individuo
    """
    
    x0=np.array([[N1-10, N2 ],[10,0],[0,0]],dtype=int)
    
    ## delta_s son los incrementos de tiempos. 
    ##Debe ser elegido
    ##               delta_s<min{1,1/max{R01,R02}}
    
    beta01,beta02=R01/N1,R02/N2
    
    
    
    X=np.zeros([3,2,n],dtype=int)
    X[:,:,0]=x0
    Transfer=np.zeros([3,2,n-1],dtype=int)
    I1d=np.zeros(n-1,dtype=int)
    I2d=np.zeros(n-1,dtype=int)
    
    for i in range(n-1):
        X0,I1d[i],I2d[i],T0=SIR_est_2C(X[:,:,i],beta01,beta02,media_transf,delta_s)
        X[:,:,i+1]=X0
        Transfer[:,:,i]=T0

    return X,I1d,I2d,Transfer



def SIR_est_2C(x,beta01,beta02,media_transf, delta_s):
    
    
    ## Decidir cuantos habitantes pasan de una población a otra
    """
    S1,I1,R1=x[:,0]
    S2,I2,R2=x[:,1]

    
    N1=float(S1+I1+R1)
    N2=float(S2+I2+R2)
    """
    
    N1=float(np.sum(x[:,0]))
    N2=float(np.sum(x[:,1]))
    
    Transfer1=poisson(delta_s*media_transf*x[:,0]/N1)
    Transfer2=poisson(delta_s*media_transf*x[:,1]/N2)
 
    Transfer1=np.minimum(Transfer1,x[:,0])
    Transfer2=np.minimum(Transfer2,x[:,1])
    
    Transfer=np.vstack((Transfer1,Transfer2)).T
    
    
    x[:,0]=Transfer2-Transfer1+x[:,0]
    x[:,1]=Transfer1-Transfer2+x[:,1]
    S1,I1,R1=x[:,0]
    S2,I2,R2=x[:,1]
    
    
    """
    mu1=beta01*delta_s*S1*I1
    mu2=delta_s*I1
    nu1=beta02*delta_s*S2*I2
    nu2=delta_s*I2
    """
    mu1=beta01*delta_s*S1
    mu2=delta_s
    nu1=beta02*delta_s*S2
    nu2=delta_s   
    
    
    I1_dot,R1_dot=np.sum(poisson(lam=(mu1,mu2),size=(I1,2)),axis=0)
    I2_dot,R2_dot=np.sum(poisson(lam=(nu1,nu2),size=(I2,2)),axis=0)

    Delta=np.array([[I1_dot,I2_dot],[R1_dot,R2_dot]])

    
    Delta=np.minimum(Delta,x[:2,:2])
    
    

    S1_new=S1-Delta[0,0]
    I1_new=I1-Delta[1,0]+Delta[0,0]
    R1_new=R1+Delta[1,0]
    
    S2_new=S2-Delta[0,1]
    I2_new=I2-Delta[1,1]+Delta[0,1]
    R2_new=R2+Delta[1,1]
    
   
    
    X=np.array([[S1_new,S2_new ],[I1_new,I2_new],[R1_new,R2_new]])
    return X,I1_dot,I2_dot, Transfer




from numpy.random import rand, binomial, multinomial, poisson


###################  EXPERIMENTO #############################################
##############################################################################

fig, ((ax1,ax2,ax3),(ax4,ax5,ax6))=plt.subplots(2,3,figsize=(20,15))

R01,R02=1.1,5.1



N1=100000
N2=100000
delta_s=.1*min(1,N1/R01,N2/R02)
media_transf=10
n=1000


X=np.zeros([3,2,n],dtype=int)
T=np.zeros([3,2,n-1],dtype=int)
I1d=np.zeros(n-1,dtype=int)
I2d=np.zeros(n-1,dtype=int)

nro_exp=1
for j in range(nro_exp):
    X1,I1d1,I2d1,T1=SIR_2C_estocastico(N1,N2,n,R01,R02,media_transf,delta_s)
    X+=X1
    T+=T1
    I1d+=I1d1
    I2d+=I2d1
X=X/nro_exp
T=T/nro_exp
I1d=I1d/nro_exp
I2d=I2d/nro_exp



s=np.arange(0,n*delta_s,delta_s)





ax1.plot(s,X[:,0,:].T,marker='o')
ax1.set(yscale='log',ylim=(1,N1+N2))
ax1.set_title('Ciudad 1')


ax2.plot(s,X[:,1,:].T,marker='o')
ax2.set(yscale='log',ylim=(1,N1+N2))
ax2.set_title('Ciudad 2')

Y=np.sum(X,axis=1) ## Suma de las dos ciudades
Ia=np.sum(Y[1:,:],axis=0) ## Infectados acumulados
Iad=np.diff(Ia)  ## infectados diarios

###  Grafica de infectados acumulados###################################

ax3.plot(s,Ia,s[1:],Iad)
ax3.set(yscale='log',ylim=(1,N1+N2))
ax3.set_title('Pais')

ax4.plot(s[:-1],T[:,0,:].T.cumsum(axis=0),marker='o')
ax4.set_title('Ciudad 1-Migraciones')

ax5.plot(s[:-1],T[:,1,:].T.cumsum(axis=0),marker='o')
ax5.set_title('Ciudad 2-Migraciones')

ax6.plot(s[:-1],I1d,s[:-1],I2d,marker='o')
ax6.set_title('Ciudadades 1 y 2-Casos nuevos')

