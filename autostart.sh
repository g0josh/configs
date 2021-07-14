#!/bin/bash

# merge theme
theme=$HOME/.config/themes/.xcolors
if [ -f $theme ]; then
    xrdb -load $theme
    xrdb -merge ~/.Xresources
fi

urxvtd &
picom --experimental-backends &
urxvt -name music -e ncmpcpp -s visualizer &
# mcc --updated-callback 'polybar-msg hook musik 1' &
