#!/bin/bash

# merge theme
theme=$HOME/.config/themes/.xcolors
if [ -f $theme ]; then
    xrdb -merge $theme
fi

numlockx on
udiskie -2 &
urxvtd &
rslync --config ~/.config/resilio-sync/config.json 
picom --experimental-backends &
urxvt -name music -e ncmpcpp &
reload-screens &
