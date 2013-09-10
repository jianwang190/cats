#!/bin/bash

for x in `seq 1 21`; do
    wget http://www.cs.qub.ac.uk/itc2007/curriculmcourse/initialdatasets/comp0$x.ctt
done
