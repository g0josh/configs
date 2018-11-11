#
# ~/.bashrc
#

# If not running interactively, don't do anything
[[ $- != *i* ]] && return

function parse_git_branch { 
   git branch --no-color 2> /dev/null | sed -e '/^[^*]/d' -e 's/* \(.*\)/(\1)/' 
} 
export PS1="\[\e[0;41m\] \A \[\e[0m\] \[\e[0;41m\] \u@\h\[\e[0m\] \[\e[0;45m\]\w\[\e[m\] \[\e[0;42m\]\$(parse_git_branch)\[\e[0m\]\n"

alias ls='ls --color=auto'
alias shut='shutdown now'

# ROS
source ~/dev/catkin_ws/devel/setup.bash
alias catkin_make='catkin_make -DPYTHON_VERSION=3.7'
