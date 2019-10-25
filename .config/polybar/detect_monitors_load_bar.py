#!/usr/bin/python3
# -*- coding: utf-8 -*-

import subprocess
import os
import sys
import json

POWER_ICONS = {'power':'','reboot':'','lock':'', 
        'logout':'', 'cancel':''}
FORMAT_PATH = '/tmp/poly_ws_formats'

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
    # get the theme file from polybar config
    with open(os.path.join(os.path.expanduser('~'),'.config','themes','current.theme'),'r') as fh:
        theme = json.load(fh)

    # Workspace formats
    formats = {}
    formats['layoutWs'] = f'%{{B{theme["background"]}}}%{{F{theme["titlebg"]}}}{theme["leftmoduleprefix"]}%{{F-}}%{{B-}}%{{B{theme["titlebg"]}}}%{{F{theme["titlefg"]}}}{" "*theme["wspadding"]}%label%{" "*theme["wspadding"]}%{{F-}}%{{B-}}%{{B{theme["background"]}}}%{{F{theme["titlebg"]}}}{theme["leftmodulesuffix"]}%{{F-}}%{{B-}}'
    formats['activeWs'] = f'%{{B{theme["background"]}}}%{{F{theme["focusedbg"]}}}{theme["leftmoduleprefix"]}%{{F-}}%{{B-}}%{{B{theme["focusedbg"]}}}%{{F{theme["focusedfg"]}}}{" "*theme["wspadding"]}%label%{" "*theme["wspadding"]}%{{F-}}%{{B-}}%{{B{theme["background"]}}}%{{F{theme["focusedbg"]}}}{theme["leftmodulesuffix"]}%{{F-}}%{{B-}}'
    formats['activeWsOther'] = f'%{{B{theme["background"]}}}%{{F{theme["bodybg"]}}}{theme["leftmoduleprefix"]}%{{F-}}%{{B-}}%{{B{theme["bodybg"]}}}%{{F{theme["focusedbg"]}}}{" "*theme["wspadding"]}%label%{" "*theme["wspadding"]}%{{F-}}%{{B-}}%{{B{theme["background"]}}}%{{F{theme["bodybg"]}}}{theme["leftmodulesuffix"]}%{{F-}}%{{B-}}'
    formats['occupiedWs'] = f'%{{B{theme["background"]}}}%{{F{theme["bodybg"]}}}{theme["leftmoduleprefix"]}%{{F-}}%{{B-}}%{{B{theme["bodybg"]}}}%{{F{theme["bodyfg"]}}}{" "*theme["wspadding"]}%label%{" "*theme["wspadding"]}%{{F-}}%{{B-}}%{{B{theme["background"]}}}%{{F{theme["bodybg"]}}}{theme["leftmodulesuffix"]}%{{F-}}%{{B-}}'
    formats['visibleWs'] = f'%{{B{theme["background"]}}}%{{F{theme["altbg"]}}}{theme["leftmoduleprefix"]}%{{F-}}%{{B-}}%{{B{theme["altbg"]}}}%{{F{theme["altfg"]}}}{" "*theme["wspadding"]}%label%{" "*theme["wspadding"]}%{{F-}}%{{B-}}%{{B{theme["background"]}}}%{{F{theme["altbg"]}}}{theme["leftmodulesuffix"]}%{{F-}}%{{B-}}'
    formats['visibleWsOther'] = f'%{{B{theme["background"]}}}%{{F{theme["bodybg"]}}}{theme["leftmoduleprefix"]}%{{F-}}%{{B-}}%{{B{theme["bodybg"]}}}%{{F{theme["altbg"]}}}{" "*theme["wspadding"]}%label%{" "*theme["wspadding"]}%{{F-}}%{{B-}}%{{B{theme["background"]}}}%{{F{theme["bodybg"]}}}{theme["leftmodulesuffix"]}%{{F-}}%{{B-}}'
    formats['urgetWs'] = f'%{{B{theme["background"]}}}%{{F{theme["urgentbg"]}}}{theme["leftmoduleprefix"]}%{{F-}}%{{B-}}%{{B{theme["urgentbg"]}}}%{{F{theme["urgentfg"]}}}{" "*theme["wspadding"]}%label%{" "*theme["wspadding"]}%{{F-}}%{{B-}}%{{B{theme["background"]}}}%{{F{theme["urgentbg"]}}}{theme["leftmodulesuffix"]}%{{F-}}%{{B-}}'
    
    #Save formats for qtile and other scripts to access
    with open(FORMAT_PATH, 'w') as fh:
        json.dump(formats, fh)
    poly_vars = {}
    # power menu widgets
    poly_vars["poweropen"]= f'%{{B{theme["background"]}}}%{{F{theme["titlebg"]}}}{theme["rightmoduleprefix"]}%{{F-}}%{{B-}}%{{B{theme["titlebg"]}}}%{{F{theme["titlefg"]}}}{" "*theme["titlepadding"]}{POWER_ICONS["power"]}{" "*theme["titlepadding"]}%{{F-}}%{{B-}}%{{B{theme["background"]}}}%{{F{theme["titlebg"]}}}{theme["rightmoduleprefix"]}%{{F-}}%{{B-}}'
    poly_vars['powerclose']= f'%{{B{theme["background"]}}}%{{F{theme["titlebg"]}}}{theme["rightmoduleprefix"]}%{{F-}}%{{B-}}%{{B{theme["titlebg"]}}}%{{F{theme["titlefg"]}}}{" "*theme["titlepadding"]}{" "*theme["titlepadding"]}%{{F-}}%{{B-}}%{{B{theme["background"]}}}%{{F{theme["titlebg"]}}}{theme["rightmodulesuffix"]}%{{F-}}%{{B-}}'
    poly_vars['power00']= f'%{{B{theme["background"]}}}%{{F{theme["titlebg"]}}}{theme["rightmoduleprefix"]}%{{F-}}%{{B-}}%{{B{theme["titlebg"]}}}%{{F{theme["titlefg"]}}}{" "*theme["bodypadding"]}{POWER_ICONS["reboot"]}{" "*theme["bodypadding"]}%{{F-}}%{{B-}}%{{B{theme["background"]}}}%{{F{theme["titlebg"]}}}{theme["rightmodulesuffix"]}%{{F-}}%{{B-}}'
    poly_vars['power01']= f'%{{B{theme["background"]}}}%{{F{theme["titlebg"]}}}{theme["rightmoduleprefix"]}%{{F-}}%{{B-}}%{{B{theme["titlebg"]}}}%{{F{theme["titlefg"]}}}{" "*theme["bodypadding"]}{POWER_ICONS["power"]}{" "*theme["bodypadding"]}%{{F-}}%{{B-}}%{{B{theme["background"]}}}%{{F{theme["titlebg"]}}}{theme["rightmodulesuffix"]}%{{F-}}%{{B-}}'
    poly_vars['power02']= f'%{{B{theme["background"]}}}%{{F{theme["titlebg"]}}}{theme["rightmoduleprefix"]}%{{F-}}%{{B-}}%{{B{theme["titlebg"]}}}%{{F{theme["titlefg"]}}}{" "*theme["bodypadding"]}{POWER_ICONS["logout"]}{" "*theme["bodypadding"]}%{{F-}}%{{B-}}%{{B{theme["background"]}}}%{{F{theme["titlebg"]}}}{theme["rightmodulesuffix"]}%{{F-}}%{{B-}}'
    poly_vars['power03']= f'%{{B{theme["background"]}}}%{{F{theme["titlebg"]}}}{theme["rightmoduleprefix"]}%{{F-}}%{{B-}}%{{B{theme["titlebg"]}}}%{{F{theme["titlefg"]}}}{" "*theme["bodypadding"]}{POWER_ICONS["lock"]}{" "*theme["bodypadding"]}%{{F-}}%{{B-}}%{{B{theme["background"]}}}%{{F{theme["titlebg"]}}}{theme["rightmodulesuffix"]}%{{F-}}%{{B-}}'
    lan1, lan2, wlan = getInterfaces()
    connected = setupMonitors()
    _connected = {}
    for i, monitor in enumerate(connected):
        try:
            os.environ['POLY_MONITOR'] = monitor
            os.environ['POLY_POWER_OPEN'] = poly_vars['poweropen']
            os.environ['POLY_POWER_CLOSE'] = poly_vars['powerclose']
            os.environ['POLY_POWER_0-0'] = poly_vars['power00']
            os.environ['POLY_POWER_0-1'] = poly_vars['power01']
            os.environ['POLY_POWER_0-2'] = poly_vars['power02']
            os.environ['POLY_POWER_0-3'] = poly_vars['power03']
            os.environ['POLY_WLAN'] = wlan
            os.environ['POLY_LAN1'] = lan1
            os.environ['POLY_LAN2'] = lan2
            for key in theme:
                print(key.upper(), theme[key])
                os.environ['POLY_'+key.upper()] = str(theme[key])
            print(poly_vars)
            print(theme)
            #if sys.version_info[0] < 3:
            #    subprocess.call(['killall', '-q', 'polybar'])
            #    subprocess.call(['polybar', '--reload', 'island'])
            #else:
            #    subprocess.run(['killall', '-q', 'polybar'])
            #    o = subprocess.Popen('polybar -r island', shell=True)
            #    _connected[i] = {'name':monitor, 'pid':o.pid}
        except subprocess.CalledProcessError as e:
            print(e.output.decode().strip())
