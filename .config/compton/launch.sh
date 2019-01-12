#!/usr/bin/env bash

killall -q compton

while prep -u $UID -x compton >/dev/null; do sleep 0.5;done

compton --config $HOME/.config/compton/launch &

