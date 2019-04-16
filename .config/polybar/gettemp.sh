#!/bin/bash

CT=`sensors|grep temp1:|cut -d'+' -f 2 | cut -d'(' -f 1`
GT=`nvidia-smi -q -d TEMPERATURE |grep  "GPU Current Temp"| awk '{print $5}'`

echo "${CT::2}|${GT}"
