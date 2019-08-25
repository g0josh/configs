#!/bin/bash

CT=`sensors|grep CPUTIN|awk '{print $2}'`
GT=`nvidia-smi -q -d TEMPERATURE |grep  "GPU Current Temp"| awk '{print $5}'`

echo "${CT:1:2}|${GT}"
