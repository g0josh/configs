#!/bin/bash

# merge theme
theme=$HOME/.config/themes/.xcolors
if [ -f $theme ]; then
    xrdb -load $theme
    xrdb -merge ~/.Xresources
fi

# udiskie -2 &
urxvtd &
picom --experimental-backends &