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
beta=1.0# ya la multiplicamos por delta t
b=0
gama=.5
N=100 # Total population size





nro_exp=5
I=np.zeros([nro_exp,time+1],dtype=int)
S=np.zeros([nro_exp,time+1],dtype=int)
I[:,0]=2 
S[:,0]=98
#
#
for i in range(nro_exp):
   
    for j in range(time):
        p1=beta*I[i,j]*S[i,j]/N*dtt
        p2=gama*I[i,j]*dtt
        p3=b*I[i,j]*dtt
        p4=b*(N-S[i,j]-I[i,j])
        
        NumAlea=np.random.rand()
        if NumAlea<= p1:
            I[i,j+1]=I[i,j]+1
            S[i,j+1]=S[i,j]-1
        elif NumAlea<=p1+p2:
            I[i,j+1]=I[i,j]-1
            S[i,j+1]=S[i,j]
        elif NumAlea<=p1+p2+p3:
            I[i,j+1]=I[i,j]-1
            S[i,j+1]=S[i,j]+1
        elif NumAlea<=p4+p3+p2+p1:
            I[i,j+1]=I[i,j]
            S[i,j+1]=S[i,j]+1
        else:
            I[i,j+1]=I[i,j]
            S[i,j+1]=S[i,j]
    ax.plot(I[i,:])
    
I_det=np.zeros(time+1,dtype=float)
S_det=np.zeros(time+1,dtype=float)
I_det[0]=2     
S_det[0]=98


for j in range(time):
    S_det[j+1]=S_det[j]-beta*I_det[j]*S_det[j]/N*dtt+b*(N-S_det[j])*dtt
    I_det[j+1]=I_det[j]+beta*I_det[j]*S_det[j]/N*dtt- (b+gama)*I_det[j]*dtt
    
I_media=np.sum(I,axis=0)*nro_exp**(-1)
ax1.plot(I_det,linewidth=4)
ax1.plot(I_media,linewidth=4)
