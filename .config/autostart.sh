#!/bin/bash

# merge theme
theme=$HOME/.config/themes/.xcolors
if [ -f $theme ]; then
    xrdb -load $theme
    xrdb -merge ~/.Xresources
fi

# udiskie -2 &
numlockx off
urxvtd &
mpd &
urxvt -name music -e ncmpcpp -s visualizer &
picom --experimental-backends &
# mcc --updated-callback 'polybar-msg hook musik 1' &
