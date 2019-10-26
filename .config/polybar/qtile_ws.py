#!/usr/bin/python3

import sys
import json
import  subprocess

from libqtile.command import Client

LAYOUT_ICONS = {'columns':'HHH','monadtall':'[]=',
        'monadwide':'TTT','max':'[ ]','treetab':'|[]'}

def main():
    if len(sys.argv) < 3:
        sys.exit(1)

    cmd = sys.argv[1]

    client = Client()
    groups = client.groups()
    curr_group = client.group.info()
    with open('/tmp/polybar_info', 'r') as fh:
        d = json.load(fh)
    screens = d['screens']
    formats = d['formats']
    separator = d['separator']

    if cmd == 'get':
        try:
            pid = int(sys.argv[2])
        except:
            sys.exit(1)
        result = ""
        for ws in groups:
            if ws == 'scratchpad':
                continue
            if ws == curr_group['name']:
                if pid == screens[str(curr_group['screen'])]['pid']:
                    if result:
                        result = formats['layoutWs'].replace('%label%',LAYOUT_ICONS[curr_group['layout']]) + separator + result
                    else:
                        result = formats['layoutWs'].replace('%label%',LAYOUT_ICONS[curr_group['layout']])
                    result = result + separator + formats['activeWs'].replace('%label%', curr_group['label'])
                else:
                    result = result + separator + formats['activeWsOther'].replace('%label%', curr_group['label'])
            elif groups[ws]['screen'] is not None:
                if pid == screens[str(groups[ws]['screen'])]['pid']:
                    result = result + separator + formats['visibleWs'].replace('%label%', groups[ws]['label'])
                else:
                    result = result + separator + formats['visibleWsOther'].replace('%label%', groups[ws]['label'])
            elif client.groups()[ws]['windows']:
                result = result + separator + formats['occupiedWs'].replace('%label%', groups[ws]['label'])
        return result
    elif cmd == 'set':
        ws = sys.argv[2]
        if not ws.isdigit():
            _ws = int(curr_group['name'])
            if ws in ['next', '+1']:
                ws = str(_ws+1) if _ws+1 <= len(groups)-1 else '1'
            elif ws in ['prv','prev','previous','-1']:
                ws = str(_ws-1) if _ws-1 >= 1 else str(len(groups)-1)
            else:
                sys.exit(1)
        elif ws not in groups:
            sys.exit(1)
        client.group[ws].toscreen()
        try:
            subprocess.call(['polybar-msg', 'hook', 'qtileWs', '1'])
        except subprocess.CalledProcessError as e:
            print(e)

if __name__ == '__main__':
    print(main())

