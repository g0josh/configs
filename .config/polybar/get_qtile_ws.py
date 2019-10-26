#!/usr/bin/python

from __future__ import print_function
from libqtile.command import Client
import sys
import os
import json
import subprocess
import logging
fh = logging.FileHandler(filename='/home/job/log')
fh.setLevel('INFO')
logger = logging.getLogger('default')
logger.addHandler(fh)
logger.setLevel('INFO')

PID_FILE_PATH = '/tmp/polybar_pids'

def get_default_format():
    with open('/tmp/polybar_ws_formats', 'r') as f:
        formats = json.loads(f.read())
    return formats

def main():
    if len(sys.argv) < 3:
        return
    cmd = sys.argv[1]
    ws = sys.argv[2]
    pid = sys.argv[3] if len(sys.argv) == 4 else None
    if cmd not in ['get', 'set']:
        return
    if cmd == 'get' and pid is None:
        return
    client = Client()
    if ws not in client.groups():
        return
    with open(PID_FILE_PATH, 'r') as f:
        screens = json.loads(f.read())
    default_formats = get_default_format()
    if cmd == 'get':
        logger.info("got {}, {}, {}".format(cmd, ws, pid))
        if ws == client.group.info()['name']:
            _pid = str(screens[str(client.group.info()['screen'])]['pid'])
            if pid == _pid:
                result = default_formats['active']
                #result = f"{ws}active"
            else:
                result = default_formats['activeother']
                #result = f"{ws}activeother"
        elif client.groups()[ws]['screen'] is not None:
            _pid = str(screens[str(client.groups()[ws]['screen'])]['pid'])
            if pid == _pid:
                result = default_formats['visible']
                #result = f"{ws}visible"
            else:
                #result = f"{ws}visibleother"
                result = default_formats['visibleother']
        elif client.groups()[ws]['windows']:
            result = default_formats['occupied']
            #result = f"{ws}occ"
        else:
            result = ""
        if result:
            result = result.replace('%name%',client.groups()[ws]['label'])
        return result
    elif cmd == 'set':
        curr_ws = client.group.info()['name']
        client.group[ws].toscreen()
        logger.info("{}, {}".format(curr_ws, ws))
        try:
            cmd = ""
            for w in [ws, curr_ws]:
                cmd += "hook:module/qtileWs{}1\n".format(w)
            logger.info(cmd)
            for s in screens:
                with open('/tmp/polybar_mqueue.{}'.format(screens[s]['pid']), 'w') as f:
                        f.write(cmd)
                #l = 'polybar-msg hook qtileWs{} 1'.format(w)
                #l = ['polybar-msg', 'hook', 'qtileWs{}'.format(w), '1']
                #logger.info(l)
                #a=subprocess.Popen(l, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                #o, e = a.communicate()
                #logger.info("{},{}".format(o,e))
                #subprocess.call(l)
        except Exception as e:
            logger.warn(e)

if __name__ == '__main__':
    print(main())
    sys.exit(0)

