#!/usr/bin/python

from libqtile.command import Client
import sys

LAYOUT_ICONS = {'columns':'HHH','monadtall':'[]=',
        'monadwide':'TTT','max':'[ ]','treetab':'|[]'}

if __name__=='__main__':
    client = Client()
    group_info = client.group.info()
    print(LAYOUT_ICONS[group_info['layout']])
    sys.exit(0)
