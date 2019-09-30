#!/usr/bin/python

from libqtile.command import Client
import sys

client = Client()
LAYOUT_ICONS = {'columns':'HHH','monadtall':'[]=',
        'monadwide':'TTT','max':'[ ]','treetab':'|[]'}

if __name__=='__main__':
    group_info = client.group.info()
    print(LAYOUT_ICONS[group_info['layout']])
    sys.exit(0)
