#!/bin/sh
xrandr --newmode "2560x1080_60.00"  230.00  2560 2720 2992 3424  1080 1083 1093 1120 -hsync +vsync
xrandr --addmode HDMI-1 "2560x1080_60.00"
xrandr --output eDP-1 --primary --mode 1600x900 --pos 2560x0 --rotate normal --output DP-1 --off --output HDMI-1 --mode 2560x1080_60.00 --pos 0x0 --rotate normal --output DP-2 --off --output HDMI-2 --off --output DisplayPort-1-2 --off --output DisplayPort-1-3 --off
