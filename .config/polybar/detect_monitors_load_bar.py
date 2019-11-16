#!/usr/bin/python3
# -*- coding: utf-8 -*-

import subprocess
import os
import sys
import json
import yaml

POWER_ICONS = {'power':'','reboot':'','lock':'', 
        'logout':'', 'cancel':''}
POLY_INFO_PATH = '/tmp/polybar_info'
PARSED_THEME_PATH = os.path.expanduser('~/.config/themes/theme')

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
    with open(PARSED_THEME_PATH, 'r') as fh:
        theme = yaml.safe_load(fh)
    if 'occupiedbg' not in theme:
        theme['occupiedbg'] = theme['bodybg']
    if 'occupiedfg' not in theme:
        theme['occupiedfg'] = theme['bodyfg']
    formats = {}
    formats['layoutWs'] = f'%{{B{theme["background"]}}}%{{F{theme["titlebg"]}}}{theme["leftmoduleprefix"]}%{{F-}}%{{B-}}%{{B{theme["titlebg"]}}}%{{F{theme["titlefg"]}}}{" "*theme["wspadding"]}%label%{" "*theme["wspadding"]}%{{F-}}%{{B-}}%{{B{theme["background"]}}}%{{F{theme["titlebg"]}}}{theme["leftmodulesuffix"]}%{{F-}}%{{B-}}'
    formats['activeWs'] = f'%{{B{theme["background"]}}}%{{F{theme["focusedbg"]}}}{theme["leftmoduleprefix"]}%{{F-}}%{{B-}}%{{B{theme["focusedbg"]}}}%{{F{theme["focusedfg"]}}}{" "*theme["wspadding"]}%label%{" "*theme["wspadding"]}%{{F-}}%{{B-}}%{{B{theme["background"]}}}%{{F{theme["focusedbg"]}}}{theme["leftmodulesuffix"]}%{{F-}}%{{B-}}'
    formats['activeWsOther'] = f'%{{B{theme["background"]}}}%{{F{theme["bodybg"]}}}{theme["leftmoduleprefix"]}%{{F-}}%{{B-}}%{{B{theme["bodybg"]}}}%{{F{theme["focusedbg"]}}}{" "*theme["wspadding"]}%label%{" "*theme["wspadding"]}%{{F-}}%{{B-}}%{{B{theme["background"]}}}%{{F{theme["bodybg"]}}}{theme["leftmodulesuffix"]}%{{F-}}%{{B-}}'
    formats['occupiedWs'] = f'%{{B{theme["background"]}}}%{{F{theme["occupiedbg"]}}}{theme["leftmoduleprefix"]}%{{F-}}%{{B-}}%{{B{theme["occupiedbg"]}}}%{{F{theme["occupiedfg"]}}}{" "*theme["wspadding"]}%label%{" "*theme["wspadding"]}%{{F-}}%{{B-}}%{{B{theme["background"]}}}%{{F{theme["occupiedbg"]}}}{theme["leftmodulesuffix"]}%{{F-}}%{{B-}}'
    formats['visibleWs'] = f'%{{B{theme["background"]}}}%{{F{theme["altbg"]}}}{theme["leftmoduleprefix"]}%{{F-}}%{{B-}}%{{B{theme["altbg"]}}}%{{F{theme["altfg"]}}}{" "*theme["wspadding"]}%label%{" "*theme["wspadding"]}%{{F-}}%{{B-}}%{{B{theme["background"]}}}%{{F{theme["altbg"]}}}{theme["leftmodulesuffix"]}%{{F-}}%{{B-}}'
    formats['visibleWsOther'] = f'%{{B{theme["background"]}}}%{{F{theme["bodybg"]}}}{theme["leftmoduleprefix"]}%{{F-}}%{{B-}}%{{B{theme["bodybg"]}}}%{{F{theme["altbg"]}}}{" "*theme["wspadding"]}%label%{" "*theme["wspadding"]}%{{F-}}%{{B-}}%{{B{theme["background"]}}}%{{F{theme["bodybg"]}}}{theme["leftmodulesuffix"]}%{{F-}}%{{B-}}'
    formats['urgetWs'] = f'%{{B{theme["background"]}}}%{{F{theme["urgentbg"]}}}{theme["leftmoduleprefix"]}%{{F-}}%{{B-}}%{{B{theme["urgentbg"]}}}%{{F{theme["urgentfg"]}}}{" "*theme["wspadding"]}%label%{" "*theme["wspadding"]}%{{F-}}%{{B-}}%{{B{theme["background"]}}}%{{F{theme["urgentbg"]}}}{theme["leftmodulesuffix"]}%{{F-}}%{{B-}}'
    
    poly_vars = {}
    # power menu widgets
    poly_vars["poweropen"]= f'%{{B{theme["background"]}}}%{{F{theme["titlebg"]}}}{theme["rightmoduleprefix"]}%{{F-}}%{{B-}}%{{B{theme["titlebg"]}}}%{{F{theme["titlefg"]}}}{" "*theme["titlepadding"]}{POWER_ICONS["power"]}{" "*theme["titlepadding"]}%{{F-}}%{{B-}}%{{B{theme["background"]}}}%{{F{theme["titlebg"]}}}{theme["rightmodulesuffix"]}%{{F-}}%{{B-}}'
    poly_vars['powerclose']= f'%{{B{theme["background"]}}}%{{F{theme["titlebg"]}}}{theme["rightmoduleprefix"]}%{{F-}}%{{B-}}%{{B{theme["titlebg"]}}}%{{F{theme["titlefg"]}}}{" "*theme["titlepadding"]}{" "*theme["titlepadding"]}%{{F-}}%{{B-}}%{{B{theme["background"]}}}%{{F{theme["titlebg"]}}}{theme["rightmodulesuffix"]}%{{F-}}%{{B-}}'
    poly_vars['reboot']= f'%{{B{theme["background"]}}}%{{F{theme["titlebg"]}}}{theme["rightmoduleprefix"]}%{{F-}}%{{B-}}%{{B{theme["titlebg"]}}}%{{F{theme["titlefg"]}}}{" "*theme["bodypadding"]}{POWER_ICONS["reboot"]}{" "*theme["bodypadding"]}%{{F-}}%{{B-}}%{{B{theme["background"]}}}%{{F{theme["titlebg"]}}}{theme["rightmodulesuffix"]}%{{F-}}%{{B-}}'
    poly_vars['poweroff']= f'%{{B{theme["background"]}}}%{{F{theme["titlebg"]}}}{theme["rightmoduleprefix"]}%{{F-}}%{{B-}}%{{B{theme["titlebg"]}}}%{{F{theme["titlefg"]}}}{" "*theme["bodypadding"]}{POWER_ICONS["power"]}{" "*theme["bodypadding"]}%{{F-}}%{{B-}}%{{B{theme["background"]}}}%{{F{theme["titlebg"]}}}{theme["rightmodulesuffix"]}%{{F-}}%{{B-}}'
    poly_vars['logout']= f'%{{B{theme["background"]}}}%{{F{theme["titlebg"]}}}{theme["rightmoduleprefix"]}%{{F-}}%{{B-}}%{{B{theme["titlebg"]}}}%{{F{theme["titlefg"]}}}{" "*theme["bodypadding"]}{POWER_ICONS["logout"]}{" "*theme["bodypadding"]}%{{F-}}%{{B-}}%{{B{theme["background"]}}}%{{F{theme["titlebg"]}}}{theme["rightmodulesuffix"]}%{{F-}}%{{B-}}'
    poly_vars['lock']= f'%{{B{theme["background"]}}}%{{F{theme["titlebg"]}}}{theme["rightmoduleprefix"]}%{{F-}}%{{B-}}%{{B{theme["titlebg"]}}}%{{F{theme["titlefg"]}}}{" "*theme["bodypadding"]}{POWER_ICONS["lock"]}{" "*theme["bodypadding"]}%{{F-}}%{{B-}}%{{B{theme["background"]}}}%{{F{theme["titlebg"]}}}{theme["rightmodulesuffix"]}%{{F-}}%{{B-}}'
    lan1, lan2, wlan = getInterfaces()
    connected = setupMonitors()
    _connected = {}
    for i, monitor in enumerate(connected):
        try:
            os.environ['POLY_MONITOR'] = monitor
            os.environ['POLY_POWER_OPEN'] = poly_vars['poweropen']
            os.environ['POLY_POWER_CLOSE'] = poly_vars['powerclose']
            os.environ['POLY_POWEROFF'] = poly_vars['poweroff']
            os.environ['POLY_REBOOT'] = poly_vars['reboot']
            os.environ['POLY_LOGOUT'] = poly_vars['logout']
            os.environ['POLY_LOCK'] = poly_vars['lock']
            os.environ['POLY_WLAN'] = wlan
            os.environ['POLY_LAN1'] = lan1
            os.environ['POLY_LAN2'] = lan2
            for key in theme:
                _key = str('POLY_'+key.upper())
                os.environ[_key] = str(theme[key])
            subprocess.call(['killall', 'polybar'])
            o = subprocess.Popen(['polybar', '-r', 'island'])
            _connected[i] = {'name':monitor, 'pid':o.pid}
        except subprocess.CalledProcessError as e:
            print(e.output.decode().strip())
    with open(POLY_INFO_PATH, 'w') as fh:
        json.dump({'formats':formats,
            'screens':_connected,'separator':theme['moduleseparator']}, fh)
