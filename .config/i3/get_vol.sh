#!/bin/bash

pactl list sinks | grep "Volume: front" | awk '{print $5}'
