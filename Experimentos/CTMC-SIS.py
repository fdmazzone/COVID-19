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

beta=1.0
b=0.25
gam=0.25
N=100.0
init=2.0
time=25.0
sim=3

for k in range(sim):
    t=np.array([0])
    i=np.array([2])
    s=N-i
    
    while i[-1]>0 and t[-1]<time:
        u2=np.random.rand() # uniform random number
        a=(beta/N)*i[-1]*s[-1]+(b+gam)*i[-1]
        probi=(beta*s[-1]/N)/(beta*s[-1]/N+b+gam)
        t=np.append(t,t[-1]+np.random.exponential(scale=1/a))
        if u2 <= probi:
            i=np.append(i,i[-1]+1)
            s=np.append(s,s[-1]-1)
        else:
            i=np.append(i,i[-1]-1)
            s=np.append(s,s[-1]+1)
    ax.plot(t,i)
    
    
    
    
    I_media=np.sum(I,axis=0)*nro_exp**(-1)
ax1.plot(I_det,linewidth=4)
ax1.plot(I_media,linewidth=4)
