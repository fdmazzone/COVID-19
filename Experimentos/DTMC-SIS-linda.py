#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Trasladado de Linda Allen, 
% MatLab Program # 1
% Discrete Time Markov Chain
% SIS Epidemic Model
% Transition Matrix and Graph of Probability Distribution

"""
time=2000
dtt=0.01 # Time step
beta=1*dtt
b=0.25*dtt
gama=0.25*dtt
N=100 # Total population size
en=50 # plot every enth time interval
T=np.zeros([N+1,N+1]) # T is the transition matrix, defiv=linspace(0,N,N+1)
v=np.linspace(0,N,N+1)
p=np.zeros([time+1,N+1])
p[0,2]=1 # Two individuals initially infected.
bt=beta*v*(N-v)/N

dt=(b+gama)*v
for i in range(1,N): # Define the transition matrix
    T[i,i]=1-bt[i]-dt[i] # diagonal entries
    T[i,i+1]=dt[i+1] # superdiagonal entries
    T[i+1,i]=bt[i] # subdiagonal entries

T[0,0]=1
T[0,1]=dt[1]
T[N,N]=1-dt[N]
for t in range(1,time+1):
    y=T.dot(p[t-1,:].T)
    p[t,:]=y.T

I=range(0,time,en)
pm=p[I,:]


ti=np.linspace(0,time,time/en)
st=np.linspace(0,N,N+1)

X, Y = np.meshgrid( st,ti)

fig = plt.figure()
ax = fig.gca(projection='3d')

surf = ax.plot_surface(X,Y, pm)




ax.set_xlabel("Number of Infectives")
ax.set_ylabel("Time Steps")
ax.set_zlabel("Probability")

"""
Trasladado de Linda Allen, 
% MatLab Program # 1
Continuous Time Markov Chain
SIS Epidemic Model
Three Sample Paths and the Deterministic Solution


"""
beta=1;
b=0.25;
gam=0.25;
N=100;

init=2;
time=25;
sim=3;

for k=1:sim
    clear t s i
    t(1)=0;
    i(1)=init;
    s(1)=N-init;
    j=1;
    while i(j)>0 & t(j)<time
        u1=rand; % uniform random number
        u2=rand; % uniform random number
        a=(beta/N)*i(j)*s(j)+(b+gam)*i(j)
        probi=(beta*s(j)/N)/(beta*s(j)/N+gam)
        t(j+1)=t(j)-log(u1)/a;
        if u2 <= probi
            i(j+1)=i(j)+1;
            s(j+1)=s(j)-1;
        else
            i(j+1)=i(j)-1;
            s(j+1)=s(j)+1;
        j=j+1;
    plot(t,i,’r-’,’LineWidth’,2)
    hold on
