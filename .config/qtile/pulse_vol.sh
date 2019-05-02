#!/bin/bash
sink=`pactl list short sinks|grep RUNNING|awk '{print $1}'`
if test -z "$sink"; then
  pactl set-sink-volume 0 $1
  pactl set-sink-volume 1 $1
else
  pactl set-sink-volume $sink $1  
fi
