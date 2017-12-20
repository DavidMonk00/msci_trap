from glob import glob
import csv
import os

def convertFile(inputfile):
    filename = ('.').join(inputfile.split('.')[:-1])
    csvfile = open(filename+".csv", 'w')
    fieldwriter = csv.writer(csvfile, delimiter=',',quotechar='|', quoting=csv.QUOTE_MINIMAL)
    for line in open(inputfile):
        line = line.strip()
        if (line[0] != "%"):
            line = list(filter(None,line.split(" ")))
            new_line = []
            for string in line:
                if (string != "NaN"):
                    new_line.append(float(string))
                else:
                    new_line.append(0.0)
            fieldwriter.writerow(new_line)
    csvfile.close()

def concatinateFiles(inputfile):
    full_file = open(inputfile, "a")
    parameter = ("_").join(inputfile.split("_")[1:])
    for line in open("gridsurface_" + parameter):
        full_file.write(line)
    os.remove("gridsurface_" + parameter)
    for line in open("gridline_" + parameter):
        full_file.write(line)
    os.remove("gridline_" + parameter)
    full_file.close()

def main():
    print "Converting to csv..."
    for i in glob("*.txt"):
        convertFile(i)
    print "Concatinating files..."
    for i in glob("grid_*.csv"):
        concatinateFiles(i)
    print "Removing original text files..."
    for i in glob("*.txt"):
        os.remove(i)
    print "Done."

if (__name__ == "__main__"):
    main()
