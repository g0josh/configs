#
# ~/.bashrc
#

# If not running interactively, don't do anything
[[ $- != *i* ]] && return

function parse_git_branch { 
   git branch --no-color 2> /dev/null | sed -e '/^[^*]/d' -e 's/* \(.*\)/(\1)/' 
} 
export PS1="\[\e[30;41m\] \A \[\e[0m\] \[\e[30;41m\] \u@\h \[\e[0m\] \[\e[0;45m\]\w\[\e[m\] \[\e[30;46m\]\$(parse_git_branch)\[\e[0m\]\n"
alias ls='ls --color=auto'
alias shut='shutdown now'
alias m='tmux new -s'
alias ma='tmux attach -t'
alias ml='tmux ls'

# ROS
alias roslocal='source ~/dev/catkin_ws/devel/setup.bash;export ROS_MASTER_URI=http://localhost:11311'
export PATH=$PATH:/usr/local/cuda/bin
export LD_LIBRARY_PATH=/usr/local/cuda/lib64

# >>> conda initialize >>>
# !! Contents within this block are managed by 'conda init' !!
__conda_setup="$('/home/job/miniconda2/bin/conda' 'shell.bash' 'hook' 2> /dev/null)"
if [ $? -eq 0 ]; then
    eval "$__conda_setup"
else
    if [ -f "/home/job/miniconda2/etc/profile.d/conda.sh" ]; then
        . "/home/job/miniconda2/etc/profile.d/conda.sh"
    else
        export PATH="/home/job/miniconda2/bin:$PATH"
    fi
fi
unset __conda_setup
# <<< conda initialize <<<

