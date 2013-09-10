#!/bin/bash

for x in `seq 1 21`; do
    if [[ $x -lt 10 ]]; then
        wget http://www.cs.qub.ac.uk/itc2007/curriculmcourse/initialdatasets/comp0$x.ctt
    else
        wget http://www.cs.qub.ac.uk/itc2007/curriculmcourse/initialdatasets/comp$x.ctt
    fi
done
