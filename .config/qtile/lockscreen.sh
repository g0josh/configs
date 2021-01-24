#!/bin/sh

LOCKIMAGE=~/Pictures/Lockscreen
if [ ! -f "$LOCKIMAGE" ]; then
#  convert ~/Pictures/Wallpaper -filter Gaussian -resize 5% -define filter:sigma=2.5 -resize 4000% ~/Pictures/Lockscreen
  convert ~/Pictures/Wallpaper -resize 2560x1080 ~/Pictures/Lockscreen
fi

C=#00000000
T="`xrdb -query|grep "*.foreground:"|awk '{print $2}'`aa"	#Text
D="`xrdb -query|grep "*.foreground:"|awk '{print $2}'`aa"	#Default
W="`xrdb -query|grep "*.foreground:"|awk '{print $2}'`aa"	#Wrong

i3lock \
--tiling \
--image $LOCKIMAGE \
 \
--radius=90 \
--ring-width=10 \
--ringcolor=$C \
--ringwrongcolor=$C \
--ringvercolor=$C \
--keyhlcolor=$D	\
--bshlcolor=$W \
--insidecolor=$C \
--insidevercolor=$C \
--insidewrongcolor=$C \
--line-uses-inside \
--indpos="450:850" \
 \
--clock \
--timecolor=$T \
--timestr="%I:%M %p" \
--timesize=200 \
--time-font="Iosevka" \
--timepos="450:1150" \
 \
--datestr="%d %b, %A" \
--datesize=100 \
--datecolor=$T \
--date-font="Iosevka" \
--datepos="450:1250" \
 \
--veriftext="" \
--verifcolor=$T \
--verifsize=140 \
--verif-font="Font Awesome 5 Free Solid" \
 \
--wrongtext="" \
--wrongcolor=$W \
--wrongsize=140	\
--wrong-font="Font Awesome 5 Free Solid" \
 \
--noinputtext="!" \
 \
--screen 1 \
