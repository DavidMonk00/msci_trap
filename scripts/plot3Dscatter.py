from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.mlab as mlab

data = np.loadtxt("./TrapRatio_mutEW_mutBiasSep_voltageRatio.analysis",delimiter=",")
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

m = np.amax(data[:,3])
print m
for i in data:
    if i[3] == m:
        ax.scatter(i[0],i[1],i[2],c='r',marker='^')

half_sigma = np.amax(data[:,3]) - 2*np.std(data[:,3])/2
dat_half_sigma = []
for i in data:
    if i[3] > half_sigma and i[3] != m:
        dat_half_sigma.append(i)


one_sigma = np.amax(data[:,3]) - 2*np.std(data[:,3])
dat_one_sigma = []
for i in data:
    if i[3] > one_sigma and i[3] <= half_sigma:
        dat_one_sigma.append(i)

#print dat_one_sigma

dat_half_sigma = np.array(dat_half_sigma)
ax.scatter(dat_half_sigma[:,0],dat_half_sigma[:,1],dat_half_sigma[:,2],c='g',marker='o')
dat_one_sigma = np.array(dat_one_sigma)
ax.scatter(dat_one_sigma[:,0],dat_one_sigma[:,1],dat_one_sigma[:,2],c='b',marker='o')

ax.set_xlabel('mutEW')
ax.set_ylabel('mutBiasSep')
ax.set_zlabel('voltageRatio')
ax.set_xlim(0.10,0.25)
ax.set_ylim(1.2,3.0)
ax.set_zlim(0.2,0.44)
plt.show()

x = data[:,3]
plt.hist(x,bins=20)
#plt.show()
