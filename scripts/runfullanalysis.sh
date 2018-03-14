#!/bin/bash
P=~/COMSOL/Data/scripts
python $P/win_field_converter.py
python $P/runanalysis.py -r './grid*.csv'
mkdir ./Analysed
mv grid_*.csv ./Analysed/
#python $P/plotscatter.py -i ./TrapRatio_*.analysis
