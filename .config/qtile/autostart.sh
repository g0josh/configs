#!/bin/bash

feh --bg-fill ~/Pictures/Wallpaper --no-fehbg
python ~/.config/i3/detect_monitors_load_bar.py &
compton &

