#!/bin/bash

CP=$(pgrep -f "urxvt -name calculator"|awk 'NR==2')
if [[ $CP ]]; then
	kill $CP
else
	i3-msg "exec urxvt -name calculator -e python"
fi
