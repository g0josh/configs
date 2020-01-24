#!/bin/bash

urxvtd &
killall compton 
feh --bg-fill ~/Pictures/Wallpaper --no-fehbg
reload-screens
compton &

