#!/bin/bash

urxvtd &
killall compton 
feh --bg-fill ~/Pictures/Wallpaper --no-fehbg
python3 ~/.config/polybar/detect_monitors_load_bar.py
compton &

