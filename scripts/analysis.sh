#!/bin/bash
for i in */ ; do
    echo $i
    cd $i
    ../../scripts/runfullanalysis.sh
    cd ..
done
