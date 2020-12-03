#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Trasladado de Linda Allen, 
% MatLab Program # 1
% Discrete Time Markov Chain
% SIS Epidemic Model
% Transition Matrix and Graph of Probability Distribution

"""


fig, (ax,ax1) = plt.subplots(1,2)

time=2000
dtt=0.01 # Time step
beta=1*dtt# ya la multiplicamos por delta t
b=0.25*dtt
gama=0.25*dtt
N=100 # Total population size


H=np.linspace(0,N,N+1)
bt=beta*H*(N-H)/N
dt=(b+gama)*H

nro_exp=500
I=np.zeros([nro_exp,time+1],dtype=int)
I[:,0]=2 
#
#
for i in range(nro_exp):
   
    for j in range(1,time+1):
        p0i=bt[I[i,j-1]]
        p1i=dt[I[i,j-1]]
        NumAlea=np.random.rand()
        if NumAlea<= p0i:
            I[i,j]=I[i,j-1]+1
        elif NumAlea<=p1i+p0i:
            I[i,j]=I[i,j-1]-1
        else:
            I[i,j]=I[i,j-1]
    ax.plot(I[i,:])
    
I_det=np.zeros(time+1,dtype=float)
I_det[0]=2     

for j in range(1,time+1):
    I_det[j]=beta*I_det[j-1]*(N-I_det[j-1])/N - (b+gama)*I_det[j-1]+I_det[j-1]
    
I_media=np.sum(I,axis=0)*nro_exp**(-1)
ax1.plot(I_det,linewidth=4)
ax1.plot(I_media,linewidth=4)
