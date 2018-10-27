#
# ~/.bashrc
#

# If not running interactively, don't do anything
[[ $- != *i* ]] && return

PS1="\[\e[41m\]\A\[\e[m\]\[\e[41m\] \[\e[m\]\[\e[41m\]\u\[\e[m\]\[\e[41m\]@\[\e[m\]\[\e[41m\]\h\[\e[m\]\[\e[41m\] \[\e[m\]\[\e[41m\]\W\[\e[m\]\[\e[41m\]:\[\e[m\] "

alias ls='ls --color=auto'
alias shut='shutdown now'

# ROS
source ~/dev/catkin_ws/devel/setup.bash
