#
# ~/.bashrc
#

# If not running interactively, don't do anything
[[ $- != *i* ]] && return

alias ls='ls --color=auto'
#PS1='[\u@\h \W]\$ '
PS1="\[\e[41m\]\A\[\e[m\]\[\e[41m\] \[\e[m\]\[\e[41m\]\u\[\e[m\]\[\e[41m\]@\[\e[m\]\[\e[41m\]\h\[\e[m\]\[\e[41m\] \[\e[m\]\[\e[41m\]\W\[\e[m\]\[\e[41m\]:\[\e[m\] "
