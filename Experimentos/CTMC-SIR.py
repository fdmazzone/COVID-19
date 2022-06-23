import numpy as np
from matplotlib import pyplot as plt
fig, ax = plt.subplots()

beta=1.0
b=0.0
gam=0.25
N=100.0
init=2.0
time=50.0
sim=3

for k in range(sim):
    t=np.array([0])
    i=np.array([2])
    s=N-i

    while i[-1]>0 and t[-1]<time:
        u2=np.random.rand() # uniform random number
        a=(beta/N)*i[-1]*s[-1]+b*(N-s[-1])+gam*i[-1]

        probi1=beta*s[-1]*i[-1]/N/a

        probi2=gam*i[-1]/a

        probi3=b*i[-1]/a

        probi4=b*(N-s[-1]-i[-1])/a

        t=np.append(t,t[-1]+np.random.exponential(scale=1/a))
        if u2 <= probi1:
            i=np.append(i,i[-1]+1)
            s=np.append(s,s[-1]-1)
        elif u2 <= probi1+probi2:
            i=np.append(i,i[-1]-1)
            s=np.append(s,s[-1])
        elif u2 <= probi1+probi2+probi3:
            i=np.append(i,i[-1]-1)
            s=np.append(s,s[-1]+1)
        else:
            i=np.append(i,i[-1])
            s=np.append(s,s[-1]+1)
        ax.plot(t,i)
