#!/bin/bash

feh --bg-fill ~/Pictures/Wallpaper --no-fehbg
python3 ~/.config/polybar/detect_monitors_load_bar.py
python3 ~/.config/theme/theme_alacritty.py
killall compton
compton &

