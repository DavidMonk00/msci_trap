import numpy as np
from matplotlib import pyplot as plt
import analysis

class Eccentricity:
    def __init__(self, data, limits):
        self.analysis = analysis.Analysis(data)
        self.xy = self.analysis.getXYAtMinimumZ()
        self.mask_limits = limits
    def plotXY(self,plane):
        x = np.unique(plane[:,0])
        y = np.unique(plane[:,1])
        plane_array = plane[:,3].reshape(len(x), len(y))
        plt.contour(y,x,plane_array,20)
        plt.axis('equal')
        plt.colorbar()
        plt.show()
    def plotScatter(self,contour):
        plt.scatter(contour[:,0],contour[:,1])
        plt.show()
    def maskPlane(self,xmax,ymax):
        plane = self.xy[np.where(np.abs(self.xy[:,0])<ymax)]
        return plane[np.where(np.abs(plane[:,1])<xmax)]
    def getMinimum(self,plane):
        return plane[np.where(plane[:,3] == np.amin(plane[:,3]))][0]
    def getContour(self,plane,value,error):
        return plane[np.where(np.abs(plane[:,3]-value)<(value*error))]
    def getAxes(self,contour):
        r = np.sqrt(np.sum(contour[:,:2]**2,axis=1))
        a = contour[np.argmax(r)][:2]
        angles = []
        a_norm = a/np.linalg.norm(a)
        for i in contour[:,:2]:
            angles.append(np.dot(a_norm,i/np.linalg.norm(i)))
        angles = np.abs(np.array(angles))
        b = contour[np.where(np.abs(angles == np.amin(angles)))][0][:2]
        return (a,b)
    def calculate(self,max_e,error):
        masked = self.maskPlane(self.mask_limits[0], self.mask_limits[1])
        contour = self.getContour(masked,max_e*self.getMinimum(masked)[3],error)
        axes = self.getAxes(contour)
        return np.linalg.norm(axes[0])/np.linalg.norm(axes[1])

def main():
    data = np.loadtxt("grid_mutDepth_0.4.csv",delimiter=",")
    E = Eccentricity(data,(50,70))
    dat = []
    for i in np.arange(1.05,1.3,0.001):
        dat.append((i,E.calculate(i, 0.02)))
        #print "Max E ratio: ", i,"Eccentricity: ", dat[-1][1]
    dat = np.array(dat)
    plt.plot(dat[:,0],dat[:,1])
    plt.show()

if (__name__ == "__main__"):
    main()
