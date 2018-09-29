#!/usr/bin/env bash

killall -q polybar

while prep -u $UID -x polybar >/dev/null; do sleep 1;done

polybar example &

