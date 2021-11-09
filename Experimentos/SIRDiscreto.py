#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Thu Jul 16 09:37:41 2020

@author: fernando
"""

def DiscSIR(x,R0, delta_s):
    S,I,R=x
    S_new=S-R0*delta_s*S*I
    I_new=(1-delta_s+R0*delta_s*S)*I
    R_new=R+delta_s*I
    return np.array([S_new,I_new,R_new])


def iter(x0,n,R0,delta_s):
    X=np.zeros([3,n])
    X[:,0]=x0
    for i in range(n-1):
        X[:,i+1]=DiscSIR(X[:,i],R0,delta_s)
    return X

def DiscSIR2(x,R11,R22,R12,R21, delta_s):
    S1,I1,R1=x[:,0]
    S2,I2,R2=x[:,1]
    
    S1_new=S1-R11*delta_s*S1*I1+R12*delta_s*S1*I2
    I1_new=(1-delta_s+R11*delta_s*S1)*I1+R12*delta_s*S1*I2
    R1_new=R1+delta_s*I1
    
    S2_new=S2-R22*delta_s*S2*I2+R21*delta_s*S2*I1
    I2_new=(1-delta_s+R22*delta_s*S2)*I2+R21*delta_s*S2*I1
    R2_new=R2+delta_s*I2
    
    X=np.array([[S1_new,S2_new ],[I1_new,I2_new],[R1_new,R2_new]])
    return X


def iter2(x0,n,R11,R22,R12,R21, delta_s):
    X=np.zeros([3,2,n])
    X[:,:,0]=x0
    for i in range(n-1):
        X[:,:,i+1]=DiscSIR2(X[:,:,i],R11,R22,R12,R21,delta_s)
    return X


x0=np.array([[.999, 1.0 ],[.001,0.0],[0.0,0.0]])
R11,R22=5.0,1.1
R12=.0
R21=0.00000001
delta_s=.5*min(1,1/R11)
X=iter2(x0,10000,R11,R22,R12,R21, delta_s)
Ia= X[1,0,:]+X[2,0,:]
Ia1=np.diff(Ia)
fig = plt.figure(figsize=(14,10))
    
Y=np.sum(X,axis=1)
Ia=np.sum(Y[1:,:],axis=0)
Iad=np.diff(Ia)
    ###  Grafica de infectados acumulados###################################
ax = plt.axes()
n,m,j=np.shape(X)
s=np.arange(0,j*delta_s,delta_s)
ax.plot(s,Ia,s[1:],Iad)
ax.set(yscale='log')