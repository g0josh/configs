#!/usr/bin/python
import sys
import os
import subprocess

def main():
    if sys.argv[1] not in ['set', 'get']:
        exit()
    if sys.argv[1] == 'set' and len(sys.argv) < 3:
        exit()
    if sys.argv[1] == 'set':
        with open('/tmp/i3-split-mode', 'w') as f:
            f.write(sys.argv[2])
        #get polybar pid and send msg
        try:
            pids = subprocess.check_output(['pgrep', 'polybar']).decode().strip().split('\n')
        except subprocess.CalledProcessError:
            pids = []
        print(pids)
        for pid in pids:
            try:
                subprocess.call(['polybar-msg', '-p', pid, 'hook', 'i3Prefix', '0'])
            except subprocess.CalledProcessError:
                pass 
    else:
        if not os.path.exists('/tmp/i3-split-mode'):
            return '|'
        else:
            with open('/tmp/i3-split-mode', 'r') as f:
                result = f.read()
                return result


if __name__ == '__main__':
    print(main())
    sys.exit(0)
