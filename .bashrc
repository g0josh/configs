#
# ~/.bashrc
#

# If not running interactively, don't do anything
[[ $- != *i* ]] && return

function parse_git_branch { 
   git branch --no-color 2> /dev/null | sed -e '/^[^*]/d' -e 's/* \(.*\)/ \1/' 
} 
export PS1="\[\e[30;43m\]\u@\h\[\e[0m\]\[\e[33m\]\[\e[0m\]\[\e[33m\]\w \[\e[m\]\[\e[31m\]\$(parse_git_branch)\[\e[0m\]\n"

alias shut='shutdown now'
alias ls='ls --color'
alias vim='nvim'

# Golang
export GOPATH='/home/job/dev/go'
export GOBIN=$GOPATH/bin
export PATH=$PATH:/usr/local/go/bin:$GOBIN

# ROS
export ROS_PYTHON_VERSION=3
alias roslocal='source ~/dev/catkin_ws/devel/setup.bash;export ROS_MASTER_URI=http://localhost:11311'
#alias rosreem='source ~/dev/catkin_ws/devel/setup.bash; export ROS_MASTER_URI=http://10.68.1.240:11311; export ROS_IP=10.68.1.151'
#export PATH=$PATH:/usr/local/cuda/bin
#export LD_LIBRARY_PATH=/usr/local/cuda/lib64
