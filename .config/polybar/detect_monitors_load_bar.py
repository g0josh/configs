#!/usr/bin/python3
# -*- coding: utf-8 -*-

import subprocess
import os
import sys
import json

POWER_ICONS = {'power':'','reboot':'','lock':'', 'logout':''}

def getInterfaces():
    lan1 = lan2 = wlan = ""
    for w in os.listdir('/sys/class/net'):
        if w.startswith('w'):
            wlan = w
        elif w.startswith('e'):
            if lan1:
                lan2 = w
            else:
                lan1 = w
    return lan1, lan2, wlan

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
                'rightmoduleprefix':"",'rightmodulesuffix':"",
                'background':'#00000000', 'wspadding':0,
                'titlepadding':0}
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
        vars['wspadding'] = int(vars['wspadding'])
        vars['titlepadding'] = int(vars['titlepadding'])
        vars['bodypadding'] = int(vars['bodypadding'])
    except Exception as e:
        vars['wspadding'] = 0
        vars['titlepadding'] = 0
        vars['bodypadding'] = 0
    # i3 workspace widgets
    poly_vars['i3focused'] = '%[B{}]%[F{}]{}%[F-]%[B-]%[B{}]%[F{}]{}%index% %icon%{}%[F-]%[B-]%[B{}]%[F{}]{}%[F-]%[B-]'.format(vars['background'],
            vars['focusedbg'],vars['leftmoduleprefix'],vars['focusedbg'],vars['focusedfg'],
            " "*vars['wspadding']," "*vars['wspadding'],vars['background'],vars['focusedbg'],
            vars['leftmodulesuffix'])
    poly_vars['ewmhactive'] = '%[B{}]%[F{}]{}%[F-]%[B-]%[B{}]%[F{}]{}%index% %icon%{}%[F-]%[B-]%[B{}]%[F{}]{}%[F-]%[B-]'.format(vars['background'],
            vars['focusedbg'],vars['leftmoduleprefix'],vars['focusedbg'],vars['focusedfg'],
            " "*vars['wspadding']," "*vars['wspadding'],vars['background'],vars['focusedbg'],
            vars['leftmodulesuffix'])

    poly_vars['i3unfocused'] = '%[B{}]%[F{}]{}%[F-]%[B-]%[B{}]%[F{}]{}%index% %icon%{}%[F-]%[B-]%[B{}]%[F{}]{}%[F-]%[B-]'.format(vars['background'],
            vars['bodybg'],vars['leftmoduleprefix'],vars['bodybg'],vars['bodyfg'],
            " "*vars['wspadding']," "*vars['wspadding'],vars['background'],
            vars['bodybg'],vars['leftmodulesuffix'])
    poly_vars['ewmhoccupied'] = '%[B{}]%[F{}]{}%[F-]%[B-]%[B{}]%[F{}]{}%index% %icon%{}%[F-]%[B-]%[B{}]%[F{}]{}%[F-]%[B-]'.format(vars['background'],
            vars['bodybg'],vars['leftmoduleprefix'],vars['bodybg'],vars['bodyfg'],
            " "*vars['wspadding']," "*vars['wspadding'],vars['background'],
            vars['bodybg'],vars['leftmodulesuffix'])

    poly_vars['i3visible']= '%[B{}]%[F{}]{}%[F-]%[B-]%[B{}]%[F{}]{}%index% %icon%{}%[F-]%[B-]%[B{}]%[F{}]{}%[F-]%[B-]'.format(vars['background'],
            vars['bodybg'],vars['leftmoduleprefix'],vars['bodybg'],vars['focusedfg'],
            " "*vars['wspadding']," "*vars['wspadding'],vars['background'],
            vars['bodybg'],vars['leftmodulesuffix'])
    poly_vars['ewmhempty']= '%[B{}]%[F{}]{}%[F-]%[B-]%[B{}]%[F{}]{}%index% %icon%{}%[F-]%[B-]%[B{}]%[F{}]{}%[F-]%[B-]'.format(vars['background'],
            vars['bodybg'],vars['leftmoduleprefix'],vars['bodybg'],vars['focusedfg'],
            " "*vars['wspadding']," "*vars['wspadding'],vars['background'],
            vars['bodybg'],vars['leftmodulesuffix'])

    poly_vars['i3urgent']= '%[B{}]%[F{}]{}%[F-]%[B-]%[B{}]%[F{}]{}%index% %icon%{}%[F-]%[B-]%[B{}]%[F{}]{}%[F-]%[B-]'.format(vars['background'],
            vars['urgentbg'],vars['leftmoduleprefix'],vars['urgentbg'],vars['urgentfg'],
            " "*vars['wspadding']," "*vars['wspadding'],vars['background'],
            vars['urgentbg'],vars['leftmodulesuffix'])
    poly_vars['ewmhurgent']= '%[B{}]%[F{}]{}%[F-]%[B-]%[B{}]%[F{}]{}%index% %icon%{}%[F-]%[B-]%[B{}]%[F{}]{}%[F-]%[B-]'.format(vars['background'],
            vars['urgentbg'],vars['leftmoduleprefix'],vars['urgentbg'],vars['urgentfg'],
            " "*vars['wspadding']," "*vars['wspadding'],vars['background'],
            vars['urgentbg'],vars['leftmodulesuffix'])
    # power menu widgets
    poly_vars['poweropen']= '%[B{}]%[F{}]{}%[F-]%[B-]%[B{}]%[F{}]{}{}{}%[F-]%[B-]%[B{}]%[F{}]{}%[F-]%[B-]'.format(vars['background'],
            vars['titlebg'],vars['rightmoduleprefix'],vars['titlebg'],vars['titlefg'],
            " "*vars['titlepadding'],POWER_ICONS['power']," "*vars['titlepadding'],vars['background'],
            vars['titlebg'],vars['rightmodulesuffix'])
    poly_vars['powerclose']= '%[B{}]%[F{}]{}%[F-]%[B-]%[B{}]%[F{}]{}{}%[F-]%[B-]%[B{}]%[F{}]{}%[F-]%[B-]'.format(vars['background'],
            vars['titlebg'],vars['rightmoduleprefix'],vars['titlebg'],vars['titlefg'],
            " "*vars['titlepadding']," "*vars['titlepadding'],vars['background'],
            vars['titlebg'],vars['rightmodulesuffix'])
    poly_vars['power00']= '%[B{}]%[F{}]{}%[F-]%[B-]%[B{}]%[F{}]{}{}{}%[F-]%[B-]%[B{}]%[F{}]{}%[F-]%[B-]'.format(vars['background'],
            vars['titlebg'],vars['rightmoduleprefix'],vars['titlebg'],vars['titlefg'],
            " "*vars['bodypadding'],POWER_ICONS['reboot']," "*vars['bodypadding'],vars['background'],
            vars['titlebg'],vars['rightmodulesuffix'])
    poly_vars['power01']= '%[B{}]%[F{}]{}%[F-]%[B-]%[B{}]%[F{}]{}{}{}%[F-]%[B-]%[B{}]%[F{}]{}%[F-]%[B-]'.format(vars['background'],
            vars['titlebg'],vars['rightmoduleprefix'],vars['titlebg'],vars['titlefg'],
            " "*vars['bodypadding'],POWER_ICONS['power']," "*vars['bodypadding'],vars['background'],
            vars['titlebg'],vars['rightmodulesuffix'])
    poly_vars['power02']= '%[B{}]%[F{}]{}%[F-]%[B-]%[B{}]%[F{}]{}{}{}%[F-]%[B-]%[B{}]%[F{}]{}%[F-]%[B-]'.format(vars['background'],
            vars['titlebg'],vars['rightmoduleprefix'],vars['titlebg'],vars['titlefg'],
            " "*vars['bodypadding'],POWER_ICONS['logout']," "*vars['bodypadding'],vars['background'],
            vars['titlebg'],vars['rightmodulesuffix'])
    poly_vars['power03']= '%[B{}]%[F{}]{}%[F-]%[B-]%[B{}]%[F{}]{}{}{}%[F-]%[B-]%[B{}]%[F{}]{}%[F-]%[B-]'.format(vars['background'],
            vars['titlebg'],vars['rightmoduleprefix'],vars['titlebg'],vars['titlefg'],
            " "*vars['bodypadding'],POWER_ICONS['lock']," "*vars['bodypadding'],vars['background'],
            vars['titlebg'],vars['rightmodulesuffix'])
    poly_vars['power10']= '%[B{}]%[F{}]{}%[F-]%[B-]%[B{}]%[F{}]{}{}{}%[F-]%[B-]%[B{}]%[F{}]{}%[F-]%[B-]'.format(vars['background'],
            vars['titlebg'],vars['rightmoduleprefix'],vars['titlebg'],vars['titlefg'],
            " "*vars['bodypadding'],POWER_ICONS['reboot']," "*vars['bodypadding'],vars['background'],
            vars['titlebg'],vars['rightmodulesuffix'])
    poly_vars['power20']= '%[B{}]%[F{}]{}%[F-]%[B-]%[B{}]%[F{}]{}{}{}%[F-]%[B-]%[B{}]%[F{}]{}%[F-]%[B-]'.format(vars['background'],
            vars['titlebg'],vars['rightmoduleprefix'],vars['titlebg'],vars['titlefg'],
            " "*vars['bodypadding'],POWER_ICONS['power']," "*vars['bodypadding'],vars['background'],
            vars['titlebg'],vars['rightmodulesuffix'])
    poly_vars['power30']= '%[B{}]%[F{}]{}%[F-]%[B-]%[B{}]%[F{}]{}{}{}%[F-]%[B-]%[B{}]%[F{}]{}%[F-]%[B-]'.format(vars['background'],
            vars['titlebg'],vars['rightmoduleprefix'],vars['titlebg'],vars['titlefg'],
            " "*vars['bodypadding'],POWER_ICONS['logout']," "*vars['bodypadding'],vars['background'],
            vars['titlebg'],vars['rightmodulesuffix'])
    for i in poly_vars:
        poly_vars[i] = poly_vars[i].replace('[','{')
        poly_vars[i] = poly_vars[i].replace(']','}')
    lan1, lan2, wlan = getInterfaces()
    _connected = {}
    for i, monitor in enumerate(connected):
        try:
            os.environ['POLY_MONITOR'] = monitor
            os.environ['POLY_I3FOCUSED'] = poly_vars['i3focused']
            os.environ['POLY_I3UNFOCUSED'] = poly_vars['i3unfocused']
            os.environ['POLY_I3VISIBLE'] = poly_vars['i3visible']
            os.environ['POLY_I3URGENT'] = poly_vars['i3urgent']
            os.environ['POLY_EWMHACTIVE'] = poly_vars['ewmhactive']
            os.environ['POLY_EWMHOCCUPIED'] = poly_vars['ewmhoccupied']
            os.environ['POLY_EWMHEMPTY'] = poly_vars['ewmhempty']
            os.environ['POLY_EWMHURGENT'] = poly_vars['ewmhurgent']
            os.environ['POLY_THEME_FILE'] = theme_path
            os.environ['POLY_POWER_OPEN'] = poly_vars['poweropen']
            os.environ['POLY_POWER_CLOSE'] = poly_vars['powerclose']
            os.environ['POLY_POWER_0-0'] = poly_vars['power00']
            os.environ['POLY_POWER_0-1'] = poly_vars['power01']
            os.environ['POLY_POWER_0-2'] = poly_vars['power02']
            os.environ['POLY_POWER_0-3'] = poly_vars['power03']
            os.environ['POLY_POWER_1-0'] = poly_vars['power10']
            os.environ['POLY_POWER_2-0'] = poly_vars['power20']
            os.environ['POLY_POWER_3-0'] = poly_vars['power30']
            os.environ['POLY_WLAN'] = wlan
            os.environ['POLY_LAN1'] = lan1
            os.environ['POLY_LAN2'] = lan2
            if sys.version_info[0] < 3:
                subprocess.call(['killall', '-q', 'polybar'])
                subprocess.call(['polybar', '--reload', 'island'])
            else:
                subprocess.run(['killall', '-q', 'polybar'])
                o = subprocess.Popen(['polybar', '--reload', 'island'])
                _connected[i] = {'name':monitor, 'pid':o.pid}
        except subprocess.CalledProcessError as e:
            print(e.output.decode().strip())
    with open('/tmp/polybars', 'w') as f:
        f.write(json.dumps(_connected))
