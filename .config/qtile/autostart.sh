#!/bin/bash

feh --bg-fill ~/Pictures/Wallpaper --no-fehbg
python3 ~/.config/polybar/detect_monitors_load_bar.py
python3 ~/.config/alacritty/color_schemes.py
killall compton
compton &

