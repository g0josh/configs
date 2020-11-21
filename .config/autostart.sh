#!/bin/bash

killall compton &

# merge theme
theme=$HOME/.config/themes/.xcolors
if [ -f $theme ]; then
    xrdb -merge $theme
fi

numlockx on
udiskie -2 &
urxvtd &
compton &
reload-screens
