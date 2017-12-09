from glob import glob
import numpy as np
import os, errno
from shutil import copyfile
import tools

class Sort:
    def __init__(self, parameters):
        self.parameters = parameters
        path = "./*"
        for i in parameters:
            path += (i + "*")
        path += ".csv"
        self.filenames = glob(path)
        self.filenames.sort()
        self.types = []
        for line in open(self.filenames[0]):
            values = line.strip().split(",")
            for i in values:
                self.types.append(float if (len(tools.getDotsInString(i)) > 0) else int)
            break
        print self.types
        self.data = np.array([[[float(j) for j in line.strip().split(",")] for line in open(i)] for i in self.filenames])
    def removeBadZmin(self):
        self.good_min_data = []
        max_z = np.amax(self.data[1][:,len(self.parameters)])
        for i in self.data[1]:
            if (i[len(self.parameters)] != 0 and i[len(self.parameters)] != max_z):
                self.good_min_data.append(i[0:len(self.parameters)])
        print self.good_min_data[0]
    def removeBadTraps(self):
        self.removeBadZmin()
        self.good_data = []
        for i in self.good_min_data:
            index = np.where(np.all(self.data[0][:,0:len(self.parameters)] == i,axis=1))
            if (self.data[0][index,len(self.parameters)] > 0):
                self.good_data.append(i)
        print self.good_data[0]
    def getGoodFiles(self):
        self.files = []
        for i in self.good_data:
            filename = "grid_"
            for j in range(len(self.parameters)):
                filename += (self.parameters[j] + "_" + str(self.types[j](i[j])) + "_")
            self.files.append(filename[:-1]+".txt")
        print self.files
    def copyGoodFiles(self):
        directory = "./"
        for i in self.parameters:
            directory += i + "_"
        directory = directory[:-1]
        try:
            os.makedirs(directory)
        except OSError as e:
            if e.errno != errno.EEXIST:
                raise
        for i in self.files:
            copyfile("./Sweeps/"+i, directory+"/"+i)

def main():
    S = Sort(["aspectratio"])
    S.removeBadTraps()
    S.getGoodFiles()
    S.copyGoodFiles()

if (__name__ == '__main__'):
    main()
