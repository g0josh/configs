#!/bin/bash

feh --bg-fill ~/Pictures/Wallpaper --no-fehbg
python ~/.config/polybar/detect_monitors_load_bar.py
killall compton
compton &

