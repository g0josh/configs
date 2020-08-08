#!/bin/bash

killall mpd &
killall compton &
numlockx on
udiskie -2 &
urxvtd &
mpd &
compton &
