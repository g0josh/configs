#!/bin/bash

CT=`sensors|grep "Package id 0:"|cut -d'+' -f 2`
GT=`nvidia-smi -q -d TEMPERATURE |grep  "GPU Current Temp"| awk '{print $5}'`

echo "${CT::2}|${GT}"
