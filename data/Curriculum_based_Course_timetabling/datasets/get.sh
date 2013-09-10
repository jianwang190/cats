#!/bin/bash

for x in `seq 1 21`; do
    [[ $x -lt 10 ]] && nr="0$x" || nr=$x 
    wget http://www.cs.qub.ac.uk/itc2007/curriculmcourse/initialdatasets/comp$nr.ctt
done
