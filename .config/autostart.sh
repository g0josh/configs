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
urxvt -e musikcube &
mcc --updated-callback 'polybar-msg hook musik 1' &
reload-screens
