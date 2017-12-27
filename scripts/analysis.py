import numpy as np
from matplotlib import pyplot as plt
from glob import glob
from scipy import signal
import pandas as pd
import tools
import argparse
import thread

x = 0
y = 1
z = 2
value = 3

def savitzky_golay(y, window_size, order, deriv=0, rate=1):
    r"""Smooth (and optionally differentiate) data with a Savitzky-Golay filter.
    The Savitzky-Golay filter removes high frequency noise from data.
    It has the advantage of preserving the original shape and
    features of the signal better than other types of filtering
    approaches, such as moving averages techniques.
    Parameters
    ----------
    y : array_like, shape (N,)
        the values of the time history of the signal.
    window_size : int
        the length of the window. Must be an odd integer number.
    order : int
        the order of the polynomial used in the filtering.
        Must be less then `window_size` - 1.
    deriv: int
        the order of the derivative to compute (default = 0 means only smoothing)
    Returns
    -------
    ys : ndarray, shape (N)
        the smoothed signal (or it's n-th derivative).
    """
    from math import factorial
    try:
        window_size = np.abs(np.int(window_size))
        order = np.abs(np.int(order))
    except ValueError, msg:
        raise ValueError("window_size and order have to be of type int")
    if window_size % 2 != 1 or window_size < 1:
        raise TypeError("window_size size must be a positive odd number")
    if window_size < order + 2:
        raise TypeError("window_size is too small for the polynomials order")
    order_range = range(order+1)
    half_window = (window_size -1) // 2
    # precompute coefficients
    b = np.mat([[k**i for i in order_range] for k in range(-half_window, half_window+1)])
    m = np.linalg.pinv(b).A[deriv] * rate**deriv * factorial(deriv)
    # pad the signal at the extremes with
    # values taken from the signal itself
    firstvals = y[0] - np.abs( y[1:half_window+1][::-1] - y[0] )
    lastvals = y[-1] + np.abs(y[-half_window-1:-1][::-1] - y[-1])
    y = np.concatenate((firstvals, y, lastvals))
    return np.convolve( m[::-1], y, mode='valid')

class Data:
    def __init__(self, filename):
        self.data = pd.read_csv(filename,delimiter=",").values
    def __getitem__(self, item):
        return self.data[item]
    def getData(self):
        return self.data

class Analysis:
    def __init__(self, data):
        arr, unique = np.unique(data[:,:3],axis = 0,return_index=True)
        self.data = data[unique]
    def loadFile(self, filename):
        self.data = Data(filename)
    def getCentralZCut(self):
        line = np.array([i for i in self.data if (i[x] == 0 and i[y] == 0)])
        line[:,value] = savitzky_golay(line[:,value],11,4)
        return line
    def getCentralMinimum(self):
        line = self.getCentralZCut()
        values = line[:,value]
        min_index = signal.argrelextrema(line[:,value],np.less)[0]
        if (len(min_index) > 0):
            return line[np.where(line[:,value] == np.amin(line[min_index][:,value]))[0]][0]
        else:
            raise Exception("No minimum")
    def getXYAtMinimumZ(self):
        z_value = 4*(int(self.getCentralMinimum()[z])/4)
        plane = np.array([i for i in self.data if i[z] == z_value])
        return plane
    def getTrapDepth(self):
        line = self.getCentralZCut()
        max_index = signal.argrelextrema(line[:,value],np.greater)[0]
        try:
            minimum = self.getCentralMinimum()
            print minimum[value]
        except Exception as e:
            return 0
        if (len(max_index) > 0):
            i = 0
            while (line[i][value] == 0):
                i += 1
            max_peaks = np.append(line[np.where(line[:,value] == np.amax(line[max_index][:,value]))[0]][0],line[i]) #Can only be one maximum due to maxwell's equations
            max_peaks = max_peaks.reshape(len(max_peaks)/4,4)
            print np.amin(max_peaks[:,value])
            return np.amin(max_peaks[:,value]) - minimum[value]
        else:
            return 0
    def getMaximumE(self):
        return np.amax(self.data[:,value])
    def getTrapRatio(self):
        return self.getTrapDepth()/self.getMaximumE()

class Eccentricity:
    def __init__(self, analysis, limits):
        self.analysis = analysis
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

class Export:
    def __init__(self,parameter):
        self.files = glob(parameter)
        self.data_files = []
        print "Loading files..."
        for filename in self.files:
            print filename
            self.data_files.append(Analysis(pd.read_csv(filename,delimiter=",").values))
    def parameter(self,filename):
        param_file = self.files[0][:tools.getDotsInString(self.files[0])[-1]]
        parameters = param_file.split("_")[1:]
        foo = filename
        for i in range(0,len(parameters),2):
            filename += (parameters[i]+"_")
        filename = filename[:-1] + ".analysis"
        f = open(filename,"a")
        for i in range(len(self.files)):
            param_file = self.files[i][:tools.getDotsInString(self.files[i])[-1]]
            parameters = param_file.split("_")[1:]
            line = ""
            for j in range(1,len(parameters),2):
                line += (parameters[j] + ",")
            if (foo == "Depth_"):
                line += (str(self.data_files[i].getTrapDepth())+"\n")
            elif (foo == "Emax_"):
                line += (str(self.data_files[i].getMaximumE())+"\n")
            elif (foo == "TrapRatio_"):
                line += (str(self.data_files[i].getTrapRatio())+"\n")
            elif (foo == "Zmin_"):
                try:
                    minimum = self.data_files[i].getCentralMinimum()
                except Exception as e:
                    minimum = [0,0,0,0]
                print minimum
                line += (str(minimum[z])+"\n")
            elif (foo == "Emin_"):
                try:
                    line += (str(self.data_files[i].getCentralMinimum()[value])+"\n")
                except Exception as e:
                    line += "0\n"
            elif (foo == "Eccentricity_"):
                try:
                    E = Eccentricity(self.data_files[i],(50,70))
                    e = E.calculate(1.2, 0.02)
                except Exception as e:
                    e = 0
                line += (str(e)+"\n")
            f.write(line)
        f.close()

def removeDuplicates():
    for f in glob("*.analysis"):
        data = pd.read_csv(f,delimiter=",").values
        arr, unique = np.unique(data[:,:3],axis = 0,return_index=True)
        np.savetxt(f, data[unique], delimiter=',')

def main():
    parser = argparse.ArgumentParser(description="Analyses COMSOL data.")
    parser.add_argument('-r', dest='regex', action='store', help='file regex')
    args = parser.parse_args()
    E = Export(args.regex)
    # print "Analysing position of minimum..."
    # E.parameter("Zmin_")
    # print "Analysing value of minimum..."
    # E.parameter("Emin_")
    # print "Analysing depth of trap..."
    # E.parameter("Depth_")
    # print "Analysing maximum E field..."
    # E.parameter("Emax_")
    # print "Analysing trap ratio..."
    # E.parameter("TrapRatio_")
    # print "Analysing eccentricity..."
    # E.parameter("Eccentricity_")
    # print "Removing duplicate entries..."
    # removeDuplicates()
    # print "Done."
    for i in E.data_files:
        line = i.getCentralZCut()
        try:
            i.getCentralMinimum()
            x = (i.getTrapDepth(), i.getTrapRatio())
            print x
            plt.scatter(line[:,z],line[:,value])
            plt.show()
        except:
            pass

if (__name__ == '__main__'):
    main()
