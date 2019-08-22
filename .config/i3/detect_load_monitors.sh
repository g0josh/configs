#!/bin/bash

mapfile -t xrandr_lines < <(xrandr --query)
xrandr_lines_index="0"
cmd="xrandr"
pos_x="0"
pos_y="x0"

while IFS= read -r line ; do
    name=$(echo $line | awk '{print $1}')
    if [[ $line == *' connected'* ]];then
        next_xrandr_line=$((xrandr_lines_index + 1))
        res_line=${xrandr_lines[next_xrandr_line]}
        if [[ $res_line =~ [0-9]{4}x[0-9]{4} ]]; then resolution="${BASH_REMATCH}"; fi
        new_x=$(echo $resolution | cut -d"x" -f1)
        cmd="$cmd --output $name --mode $resolution --pos $pos_x$pos_y --rotate normal"
        pos_x=$((pos_x + new_x))
    elif [[ $line == *'disconnected'* ]];then
        cmd="$cmd --output $name --off"
    fi
    xrandr_lines_index=$((xrandr_lines_index + 1))
done < <(xrandr --query)
$cmd
