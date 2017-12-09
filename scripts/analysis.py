import numpy as np
from matplotlib import pyplot as plt
from glob import glob
from scipy import signal
import tools
import argparse
import thread

x = 0
y = 1
z = 2
value = 3

class Data:
    def __init__(self, filename):
        self.data = np.loadtxt(filename,delimiter=",")
    def __getitem__(self, item):
        return self.data[item]
    def getData(self):
        return self.data

class Analysis:
    def __init__(self, data):
        self.data = data
    def loadFile(self, filename):
        self.data = Data(filename)
    def getCentralZcut(self):
        line = np.array([i for i in self.data if (i[x] == 0 and i[y] == 0)])
        return line
    def getCentralMinimum(self):
        line = self.getCentralZcut()
        values = line[:,value]
        min_index = signal.argrelextrema(line[:,value],np.less)[0]
        if (len(min_index) > 0):
            return line[min_index][0]
        else:
            raise Exception("No minimum")
    def getXYAtMinimumZ(self):
        z_value = self.getCentralMinimum()[z]
        plane = np.array([i for i in self.data if i[z] == z_value])
        return plane
    def getTrapDepth(self):
        line = self.getCentralZcut()
        max_index = signal.argrelextrema(line[:,value],np.greater)[0]
        try:
            minimum = self.getCentralMinimum()
        except Exception as e:
            return 0
        if (len(max_index) > 0):
            i = 0
            while (line[i][value] == 0):
                i += 1
            max_peaks = np.append(line[max_index],line[i]) #Can only be one maximum due to maxwell's equations
            max_peaks = max_peaks.reshape(len(max_peaks)/4,4)
            return np.amin(max_peaks[:,value]) - minimum[value]
        else:
            return 0
    def getMaximumE(self):
        return np.amax(self.data[:,value])
    def getTrapRatio(self):
        return self.getTrapDepth()/self.getMaximumE()

class Export:
    def __init__(self,parameter):
        self.files = glob(parameter)
        self.data_files = []
        print "Loading files..."
        for filename in self.files:
            print filename
            self.data_files.append(Analysis(np.loadtxt(filename,delimiter=",")))
    def parameter(self,filename):
        param_file = self.files[0][:tools.getDotsInString(self.files[0])[-1]]
        parameters = param_file.split("_")[1:]
        foo = filename
        for i in range(0,len(parameters),2):
            filename += (parameters[i]+"_")
        filename = filename[:-1] + ".analysis"
        f = open(filename,"w")
        for i in range(len(self.files)):
            param_file = self.files[i][:tools.getDotsInString(self.files[i])[-1]]
            parameters = param_file.split("_")[1:]
            #print parameters
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
                    minimum = self.A.getCentralMinimum()
                except Exception as e:
                    minimum = [0,0,0,0]
                line += (str(minimum[z])+"\n")
            elif (foo == "Emin_"):
                try:
                    line += (str(self.A.getCentralMinimum()[value])+"\n")
                except Exception as e:
                    line += "0\n"
            f.write(line)
        f.close()

def main():
    parser = argparse.ArgumentParser(description="Analyses COMSOL data.")
    parser.add_argument('-r', dest='regex', action='store', help='file regex')
    args = parser.parse_args()
    E = Export(args.regex)
    print "Analysing position of minimum..."
    E.parameter("Zmin_")
    print "Analysing value of minimum..."
    E.parameter("Emin_")
    print "Analysing depth of trap..."
    E.parameter("Depth_")
    print "Analysing maximum E field..."
    E.parameter("Emax_")
    print "Analysing trap ratio..."
    E.parameter("TrapRatio_")
    print "Done."

if (__name__ == '__main__'):
    main()
