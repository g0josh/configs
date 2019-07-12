#
# ~/.bashrc
#

# If not running interactively, don't do anything
[[ $- != *i* ]] && return

function parse_git_branch { 
   git branch --no-color 2> /dev/null | sed -e '/^[^*]/d' -e 's/* \(.*\)/(\1)/' 
} 
export PS1="\[\e[30;41m\] \A \[\e[0m\] \[\e[30;41m\] \u@\h \[\e[0m\] \[\e[0;45m\]\w\[\e[m\] \[\e[30;46m\]\$(parse_git_branch)\[\e[0m\]\n"

# ROS
alias roslocal='source ~/dev/catkin_ws/devel/setup.bash;export ROS_MASTER_URI=http://localhost:11311'
export PATH=$PATH:/opt/cuda/bin
export LD_LIBRARY_PATH=/opt/cuda/lib64

