#!/bin/bash

# merge theme
theme=$HOME/.config/themes/.xcolors
if [ -f $theme ]; then
    xrdb -load $theme
    xrdb -merge ~/.Xresources
fi

# check if custom screen layout exits
screen_layout_path="$HOME/.config/screen-layout.sh"
if [ -f "$screen_layout_path" ]; then
	bash "$screen_layout_path"
fi

# udiskie -2 &
urxvtd &
picom --experimental-backends &
