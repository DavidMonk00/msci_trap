import numpy as np
from glob import glob
import pandas as pd
import argparse
import export

def removeDuplicates():
    for f in sorted(glob("*.analysis")):
        data = pd.read_csv(f,delimiter=",").values
        arr, unique = np.unique(data[:,:-1],axis = 0,return_index=True)
        np.savetxt(f, data[unique], delimiter=',')

def main():
    parser = argparse.ArgumentParser(description="Analyses COMSOL data.")
    parser.add_argument('-r', dest='regex', action='store', help='file regex')
    args = parser.parse_args()
    E = export.Export(args.regex)
    E.analyse()
    print "Removing duplicate entries..."
    removeDuplicates()
    print "Done."

if (__name__ == '__main__'):
    main()
