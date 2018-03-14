import eccentricity as ecc
import analysis_seq as anlys
import tools
import numpy as np
import pandas as pd
from glob import glob

class Export:
    def __init__(self,parameter):
        self.files = sorted(glob(parameter))
        self.e = 0
    def parameter(self,filename):
        param_file = self.files[0][:tools.getDotsInString(self.files[0])[-1]]
        parameters = param_file.split("_")[1:]
        foo = filename
        for i in range(0,len(parameters),2):
            filename += (parameters[i]+"_")
        filename = filename[:-1] + ".analysis"
        f = open(filename,"a")
        param_file = self.filename[:tools.getDotsInString(self.filename)[-1]]
        parameters = param_file.split("_")[1:]
        line = ""
        for j in range(1,len(parameters),2):
            line += (parameters[j] + ",")
        if (foo == "Depth_"):
            line += (str(self.data_file.getTrapDepth())+"\n")
        elif (foo == "Emax_"):
            line += (str(self.data_file.getMaximumE())+"\n")
        elif (foo == "TrapRatio_"):
            line += (str(self.data_file.getTrapRatio())+"\n")
        elif (foo == "Zmin_"):
            minimum = self.data_file.getCentralMinimum()
            line += (str(minimum[anlys.z])+"\n")
        elif (foo == "Emin_"):
            minimum = self.data_file.getCentralMinimum()
            line += (str(minimum[anlys.value])+"\n")
        elif (foo == "Eccentricity_"):
            try:
                E = ecc.Eccentricity(self.data_file,(100,150))
                e_arr = [E.calculate(i, 0.02) for i in np.arange(1.06,1.5,0.001)]
                e = np.mean(e_arr)
            except:
                e = 0
            print e
            line += (str(e)+"\n")
            self.e = e
        elif (foo == "Quality_"):
            ratio = self.data_file.getTrapRatio()
            if (self.e == 0):
                try:
                    E = ecc.Eccentricity(self.data_file,(100,150))
                    e_arr = [E.calculate(i, 0.02) for i in np.arange(1.06,1.5,0.001)]
                    e = np.mean(e_arr)
                except:
                    e = 0
            else:
                e = self.e
            try:
                quality = float(e)/float(ratio)
            except ZeroDivisionError:
                quality = 0
            line += (str(quality)+"\n")
        f.write(line)
        f.close()
    def analyse(self):
        for filename in self.files:
            self.filename = filename
            print filename
            self.data_file = anlys.Analysis(pd.read_csv(filename,delimiter=",").values)
            print "Analysing position of minimum..."
            self.parameter("Zmin_")
            print "Analysing value of minimum..."
            self.parameter("Emin_")
            print "Analysing depth of trap..."
            self.parameter("Depth_")
            print "Analysing maximum E field..."
            self.parameter("Emax_")
            print "Analysing trap ratio..."
            self.parameter("TrapRatio_")
            print "Analysing eccentricity..."
            self.parameter("Eccentricity_")
            print "Analysing trap quality..."
            self.parameter("Quality_")
