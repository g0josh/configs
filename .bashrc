#
# ~/.bashrc
#

# If not running interactively, don't do anything
[[ $- != *i* ]] && return

function parse_git_branch { 
   git branch --no-color 2> /dev/null | sed -e '/^[^*]/d' -e 's/* \(.*\)/ \1 /' 
} 
export PS1="\[\e[30;41m\]\A\[\e[0m\] \[\e[30;41m\]\u@\h\[\e[0m\] \[\e[0;45m\]\w\[\e[m\] \[\e[30;46m\]\$(parse_git_branch)\[\e[0m\]\n"


alias shut='shutdown now'
alias ls='ls --color'
alias vim='nvim'
export EDITOR='nvim'
export VISUAL='nvim'

# ROS
alias roslocal='source ~/dev/catkin_ws/devel/setup.bash;export ROS_MASTER_URI=http://localhost:11311'
alias rosreem='source ~/dev/catkin_ws/devel/setup.bash; export ROS_MASTER_URI=http://10.68.1.240:11311; export ROS_IP=10.68.1.151'
export PATH=$PATH:/usr/local/cuda/bin
export LD_LIBRARY_PATH=/usr/local/cuda/lib64
