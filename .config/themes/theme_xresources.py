#!/usr/bin/python

import os
import yaml
import subprocess

def main():
    with open(os.path.expanduser('~/.config/themes/xresources.theme'), 'r') as fh:
        theme = yaml.safe_load(fh)
    xr_data = ""
    colors_block = False
    for key in theme['terminal_colors']:
        xr_data += '*.{}:{}\n'.format(key, theme['terminal_colors'][key])
    with open('/tmp/xr_colors', 'w') as fh:
            fh.write(xr_data)
    try:
        subprocess.call(['xrdb', '-merge', '/tmp/xr_colors'])
    except subprocess.CalledProcessError as e:
        print(e)
    #os.remove('/tmp/xr_colors')

if __name__ == '__main__':
    main()
