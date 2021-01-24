#
# ~/.bash_profile
#


[[ -f ~/.bashrc ]] && . ~/.bashrc

# Startx
if [[ ! $DISPLAY && $XDG_VTNR -eq 1 ]]; then
	startx
fi
