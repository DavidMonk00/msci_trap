#!/bin/bash
P=~/COMSOL/Data/Parameters/scripts
python $P/win_field_converter.py
python $P/analysis_seq.py -r './grid*.csv'
mkdir ./Analysed
mv grid_*.csv ./Analysed/
#python $P/plotscatter.py -i ./TrapRatio_*.analysis
