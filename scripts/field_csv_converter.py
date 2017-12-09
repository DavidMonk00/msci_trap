import csv
import argparse

parser = argparse.ArgumentParser(description="Converts data exported from COMSOL from .txt to .csv format.")
parser.add_argument('-i', dest='input', action='store', help='input file location')
parser.add_argument('-o', dest='output', action='store', help='output file location')

args = parser.parse_args()

def convert_file(inputfile, outputfile):
  with open(inputfile) as f:
    #read each line and strip newline character
    lines = [x.strip() for x in f.readlines()]
    #Removes header data
    lines = [line for line in lines if line[0] != '%']
    #split on " " and discard empty strings
    lines = [list(filter(None,line.split(" "))) for line in lines]
    # convert each value on each line into a float
    lines = [[float(string) for string in line] for line in lines]

  with open(outputfile, 'w') as csvfile:
    fieldwriter = csv.writer(csvfile, delimiter=',',quotechar='|', quoting=csv.QUOTE_MINIMAL)
    for line in lines:
      fieldwriter.writerow(line)

convert_file(args.input, args.output)
