#!/bin/sh

export PATH=$PATH:$HOME/.local/bin

# merge theme
theme=$HOME/.config/themes/.xcolors
if [ -f $theme ]; then
    xrdb -merge $theme
fi

# start WM
exec qtile
