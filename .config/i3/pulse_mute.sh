#!/bin/bash
sink=`pactl list short sinks|grep RUNNING|awk '{print $1}'`
if test -z "$sink"; then
  pactl set-sink-mute 0 $1
  pactl set-sink-mute 1 $1
else
  pactl set-sink-mute $sink $1  
fi
