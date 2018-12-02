#!/bin/bash

CT=`sensors|grep Tdie:|cut -d'+' -f 2 | cut -d'(' -f 1`
GT=`nvidia-smi -q -d TEMPERATURE |grep  GPU\ Current\ Temp| cut -d: -f2`

echo "${CT::2} | ${GT:1:3}"
