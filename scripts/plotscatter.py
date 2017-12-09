import numpy as np
from matplotlib import pyplot as plt
import argparse

parser = argparse.ArgumentParser(description="Plots scatter of data points in file.")
parser.add_argument('-i', dest='input', action='store', help='input file location')
args = parser.parse_args()
data = np.loadtxt(args.input,delimiter=",")
plt.scatter(data[:,0],data[:,1])
plt.ylim(ymin=0)
plt.xlim(0,np.amax(data[:,0]))
plt.show()
