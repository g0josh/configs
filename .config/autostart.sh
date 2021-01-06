#!/bin/bash

# merge theme
theme=$HOME/.config/themes/.xcolors
if [ -f $theme ]; then
    xrdb -merge $theme
fi

numlockx on
udiskie -2 &
urxvtd &
picom --experimental-backends &
mcc &
reload-screens
