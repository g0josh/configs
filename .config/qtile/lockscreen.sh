#!/bin/bash

gnome-screenshot -f ~/Pictures/Lockscreen
convert ~/Pictures/Lockscreen -filter Gaussian -resize 10% -define filter:sigma=4.5 -resize 2560x1080\!  ~/Pictures/Lockscreen
i3lock -i ~/Pictures/Lockscreen -t -e -f

