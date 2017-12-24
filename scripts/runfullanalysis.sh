#!/bin/bash
P=~/COMSOL/Data/Parameters/scripts
$P/preprocess.sh
python $P/analysis.py -r './grid*.csv'
mkdir ./Analysed
mv grid_*.csv ./Analysed/
#python $P/plotscatter.py -i ./TrapRatio_*.analysis
