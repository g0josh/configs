#!/bin/bash

CNT=$(pgrep -f "urxvt -name calculator"|wc -l)
if [[ $CNT -ne 0 ]]; then
	CNT=$(($CNT - 1))
	CP=$(pgrep -f "urxvt -name calculator")
	kill $CP
else
	i3-msg "exec urxvt -name calculator -e python"
fi
