#!/bin/bash
P=~/COMSOL/Data/Parameters/scripts
echo 'Removing NaNs...'
sed -i 's/NaN/0/g' ./*.txt
shopt -s nullglob
echo 'Converting to csv...'
for i in grid*.txt; do
  s=${i%.*}
  python $P/field_csv_converter.py -i $i -o $s.csv
  rm -rf $i
done
echo 'Concatinating files...'
for i in grid_*.csv; do
  PARAMETER=$(echo $i| cut -d'_' -f 2);
  VALUE=$(echo $i| cut -d'_' -f 3);
  SURFACE='gridsurface_'$PARAMETER'_'$VALUE;
  cat $i $SURFACE > 'gridfull_'$PARAMETER'_'$VALUE;
  mv 'gridfull_'$PARAMETER'_'$VALUE $i;
  LINE='gridline_'$PARAMETER'_'$VALUE;
  cat $i $LINE > 'gridfull_'$PARAMETER'_'$VALUE;
  mv 'gridfull_'$PARAMETER'_'$VALUE $i;
  rm -rf $SURFACE;
  rm -rf $LINE;
done
echo 'Done.'
