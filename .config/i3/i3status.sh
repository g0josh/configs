#!/bin/bash

i3status -c ~/.config/i3/i3status.conf | while :
do
    read line
    song="$(mpc current -f "[[%albumartist%|%artist% - ]%title%]")"
    mpd_status="$(mpc | tail -2 | head -1 | cut -d' ' -f1)"
    song_pos="$(mpc | tail -2 | head -1 | cut -d' ' -f5)"
    echo "$mpd_status  $song  $song_pos     $line" || exit1 
done
