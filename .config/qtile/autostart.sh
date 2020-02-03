#!/bin/bash

urxvtd &
killall compton 
reload-screens
compton &

