#!/usr/bin/python3
# -*- coding: utf-8 -*-

import subprocess
import os
import sys

def setupMonitors():
    try:
        o = subprocess.check_output(['xrandr']).decode()
    except subprocess.CalledProcessError as e:
        print(e.output.decode().strip())
        return

    cmd = ["xrandr"]
    connected = []
    x = 0
    for i,e in enumerate(o.split('\n')):
        if not 'connected' in e:
            continue

        name = e.strip().split()[0]
        if ' connected' in e:
            res = o.split('\n')[i+1].strip().split()[0]
            cmd += ['--output', name, '--mode', res,
                '--pos', "{}x{}".format(x, 0), '--rotate', 'normal']
            x += int(res.split('x')[0])
            connected.append(name)
        elif 'disconnected' in e:
            cmd += ['--output', name, '--off']

    try:
        if sys.version_info[0] < 3:
            subprocess.call(cmd)
        else:
            subprocess.run(cmd)
    except subprocess.CalledProcessError as e:
        print(e.output.decode().strip())
    else:
        return connected

if __name__ == '__main__':
    connected = setupMonitors()
    # get the theme file from polybar config
    theme_path = None
    with open(os.path.join(os.path.expanduser('~'),'.config','polybar','config'), 'r') as f:
        for l in f:
            if 'include-file' in l:
                theme_path = l.split('=')[-1].strip()
                break
    if not theme_path:
        print("Could not find polybar theme file")
        exit(1)
    if '~' in theme_path:
        theme_path = theme_path.replace('~', os.path.expanduser('~'))
    with open(theme_path, 'r') as f:
        vars = {'titlefg':'#000000','titlebg':'#000000',
                'bodyfg':'#000000','bodybg':'#000000',
                'urgentbg':'#000000','urgentfg':'#000000',
                'focusedbg':'#000000','focusedfg':'#000000',
                'leftmoduleprefix':"",'leftmodulesuffix':"",
                'background':'#00000000', 'i3wspadding':0}
        for i, l in enumerate(f):
            l=l.strip()
            if l.startswith('#'):
                continue
            for var in vars:
                if var in l:
                    vars[var] = l.split('=')[-1].strip()
                    break
    poly_vars = {}
    try:
        vars['i3wspadding'] = int(vars['i3wspadding'])
    except Exception as e:
        vars['i3wspadding'] = 0
    poly_vars['focused'] = '%[B{}]%[F{}]{}%[F-]%[B-]%[B{}]%[F{}]{}%index% %icon%{}%[F-]%[B-]%[B{}]%[F{}]{}%[F-]%[B-]'.format(vars['background'],
            vars['focusedbg'],vars['leftmoduleprefix'],vars['focusedbg'],vars['focusedfg'],
            " "*vars['i3wspadding']," "*vars['i3wspadding'],vars['background'],vars['focusedbg'],
            vars['leftmodulesuffix'])
    poly_vars['unfocused'] = '%[B{}]%[F{}]{}%[F-]%[B-]%[B{}]%[F{}]{}%index% %icon%{}%[F-]%[B-]%[B{}]%[F{}]{}%[F-]%[B-]'.format(vars['background'],
            vars['bodybg'],vars['leftmoduleprefix'],vars['bodybg'],vars['bodyfg'],
            " "*vars['i3wspadding']," "*vars['i3wspadding'],vars['background'],
            vars['bodybg'],vars['leftmodulesuffix'])
    poly_vars['visible']= '%[B{}]%[F{}]{}%[F-]%[B-]%[B{}]%[F{}]{}%index% %icon%{}%[F-]%[B-]%[B{}]%[F{}]{}%[F-]%[B-]'.format(vars['background'],
            vars['bodybg'],vars['leftmoduleprefix'],vars['bodybg'],vars['focusedfg'],
            " "*vars['i3wspadding']," "*vars['i3wspadding'],vars['background'],
            vars['bodybg'],vars['leftmodulesuffix'])
    poly_vars['urgent']= '%[B{}]%[F{}]{}%[F-]%[B-]%[B{}]%[F{}]{}%index% %icon%{}%[F-]%[B-]%[B{}]%[F{}]{}%[F-]%[B-]'.format(vars['background'],
            vars['urgentbg'],vars['leftmoduleprefix'],vars['urgentbg'],vars['urgentfg'],
            " "*vars['i3wspadding']," "*vars['i3wspadding'],vars['background'],
            vars['urgentbg'],vars['leftmodulesuffix'])
    for i in poly_vars:
        poly_vars[i] = poly_vars[i].replace('[','{')
        poly_vars[i] = poly_vars[i].replace(']','}')
    print(vars)
    for monitor in connected:
        try:
            os.environ['POLY_MONITOR'] = monitor
            os.environ['POLY_FOCUSED'] = poly_vars['focused']
            os.environ['POLY_UNFOCUSED'] = poly_vars['unfocused']
            os.environ['POLY_VISIBLE'] = poly_vars['visible']
            os.environ['POLY_URGENT'] = poly_vars['urgent']
            os.environ['POLY_THEME_FILE'] = theme_path
            if sys.version_info[0] < 3:
                subprocess.call(['polybar', '--reload', 'island'])
            else:
                subprocess.run(['polybar', '--reload', 'island'])
        except subprocess.CalledProcessError as e:
            print(e.output.decode().strip())

