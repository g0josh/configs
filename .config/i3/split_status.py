#!/usr/bin/python3
# -*- coding: utf-8 -*-

from __future__ import unicode_literals
import sys
import os
import subprocess

status = {'tabbed':'', 'split':'L', 'stacking':'',
        'splitv':'|','splith':'-'}
status_file = '/tmp/i3-split-mode'

def main():
    if len(sys.argv) < 2:
        return
    if sys.argv[1] not in ['set', 'get']:
        return
    if sys.argv[1] == 'set' and len(sys.argv) < 3:
        return
    curr_status = ''
    if os.path.exists(status_file):
        with open(status_file, 'r') as f:
            curr_status = f.read()
    if not curr_status:
        curr_status = 'L|'
    print(curr_status)
    if sys.argv[1] == 'set':
        if sys.argv[2] not in status:
            return
        if sys.argv[2] in ['splitv','splith']:
            #new_status = curr_status[0] + status[sys.argv[2].strip()]
            new_status = status['split'] + status[sys.argv[2].strip()]
        elif sys.argv[2] in ['tabbed','split','stacking']:
            new_status = status[sys.argv[2].strip()] + curr_status[1]
        print(new_status)
        with open('/tmp/i3-split-mode', 'w') as f:
            f.write(new_status)
        #get polybar pid and send msg
        try:
            pids = subprocess.check_output(['pgrep', 'polybar']).decode().strip().split('\n')
        except subprocess.CalledProcessError:
            pids = []
        for pid in pids:
            try:
                subprocess.call(['polybar-msg', '-p', pid, 'hook', 'i3Prefix', '1'])
            except subprocess.CalledProcessError:
                pass 
    else:
        if not os.path.exists(status_file):
            return status['splitv']
        else:
            with open(status_file, 'r') as f:
                result = f.read()
                if result[0] in [status['stacking'], status['tabbed']]:
                    return result[0]
                elif result[0] == status['split']:
                    return result[1]


if __name__ == '__main__':
    print(main())
    sys.exit(0)
