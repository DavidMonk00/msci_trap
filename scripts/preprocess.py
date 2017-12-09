from glob import glob
import tools
import os
import argparse

def main(args):
    print args.folder
    files = glob(args.folder+"*.txt")
    for f in files:
        dot_index = tools.getDotsInString(f)
        if (len(dot_index) > 2):
            filename = f[:dot_index[-1]]
            parameters = filename.split("_")[1:]
            values = []
            for i in range(1,len(parameters),2):
                values.append("%.3f"%float(parameters[i]) if (len(tools.getDotsInString(parameters[i])) > 0) else parameters[i])
            filename_new = filename.split("_")[0]
            for i in range(len(parameters)):
                if (i%2 == 0):
                    filename_new += ("_" + parameters[i])
                else:
                     filename_new += ("_" + values[i/2])
            os.rename(f, filename_new+".txt")

if (__name__ == "__main__"):
    parser = argparse.ArgumentParser(description="Sanitises COMSOL export data filenames")
    parser.add_argument('-f', dest='folder', action='store', help='folder location')
    args = parser.parse_args()
    main(args)
