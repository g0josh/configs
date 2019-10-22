
import os
import subprocess

POWER_ICONS = { 'power':'','reboot':'','lock':'', 'logout':''}
THEME_PATH = '~/.config/themes/feathers.theme'
MONITORS = ['HDMI-0']

def getTheme(path='~/.config/themes/feathers.theme'):
    result = {'titlefg':'#000000','titlebg':'#000000','bodyfg':'#000000',
             'bodybg':'#000000','focusedwindowborder':"#000000",
             'windowborder':"#000000", 'leftmoduleprefix':'',
             'leftmodulesuffix':''}
    path = os.path.expanduser(path)
    if not os.path.exists(path):
        logger.warn('Theme path does not exist- {}'.format(path))
        return result
    with open(path, 'r') as fh:
        for l in fh:
            l=l.strip()
            if l.startswith('#'):
                continue
            key, value = l.split('=')
            result[key.strip().lower()] = int(value.strip()) if value.strip().isdigit() else value.strip()
    result['activeWs'] = f'%[B{result["background"]}]%[F{result["focusedbg"]}]{result["leftmoduleprefix"]}%[F-]%[B-]%[B{result["focusedbg"]}]%[F{result["focusedfg"]}]{" "*result["wspadding"]}%label%{" "*result["wspadding"]}%[F-]%[B-]%[B{result["background"]}]%[F{result["focusedbg"]}]{result["leftmodulesuffix"]}%[F-]%[B-]'
    result['layoutWs'] = f'%[B{result["background"]}]%[F{result["titlebg"]}]{result["leftmoduleprefix"]}%[F-]%[B-]%[B{result["titlebg"]}]%[F{result["titlefg"]}]{" "*result["wspadding"]}%label%{" "*result["wspadding"]}%[F-]%[B-]%[B{result["background"]}]%[F{result["titlebg"]}]{result["leftmodulesuffix"]}%[F-]%[B-]'
    result['activeWsOther'] = f'%[B{result["background"]}]%[F{result["bodybg"]}]{result["leftmoduleprefix"]}%[F-]%[B-]%[B{result["bodybg"]}]%[F{result["focusedbg"]}]{" "*result["wspadding"]}%label%{" "*result["wspadding"]}%[F-]%[B-]%[B{result["background"]}]%[F{result["bodybg"]}]{result["leftmodulesuffix"]}%[F-]%[B-]'
    result['occupiedWs'] = f'%[B{result["background"]}]%[F{result["bodybg"]}]{result["leftmoduleprefix"]}%[F-]%[B-]%[B{result["bodybg"]}]%[F{result["bodyfg"]}]{" "*result["wspadding"]}%label%{" "*result["wspadding"]}%[F-]%[B-]%[B{result["background"]}]%[F{result["bodybg"]}]{result["leftmodulesuffix"]}%[F-]%[B-]'
    result['visibleWs'] = f'%[B{result["background"]}]%[F{result["altbg"]}]{result["leftmoduleprefix"]}%[F-]%[B-]%[B{result["altbg"]}]%[F{result["altfg"]}]{" "*result["wspadding"]}%label%{" "*result["wspadding"]}%[F-]%[B-]%[B{result["background"]}]%[F{result["altbg"]}]{result["leftmodulesuffix"]}%[F-]%[B-]'
    result['visibleWsOther'] = f'%[B{result["background"]}]%[F{result["bodybg"]}]{result["leftmoduleprefix"]}%[F-]%[B-]%[B{result["bodybg"]}]%[F{result["altbg"]}]{" "*result["wspadding"]}%label%{" "*result["wspadding"]}%[F-]%[B-]%[B{result["background"]}]%[F{result["bodybg"]}]{result["leftmodulesuffix"]}%[F-]%[B-]'
    result['UrgetWs'] = f'%[B{result["background"]}]%[F{result["urgentbg"]}]{result["leftmoduleprefix"]}%[F-]%[B-]%[B{result["urgentbg"]}]%[F{result["urgentfg"]}]{" "*result["wspadding"]}%label%{" "*result["wspadding"]}%[F-]%[B-]%[B{result["background"]}]%[F{result["urgentbg"]}]{result["leftmodulesuffix"]}%[F-]%[B-]'
    for x in result:
        if isinstance(result[x], str) and 'Ws' in x:
            result[x] = result[x].replace('[', '{')
            result[x] = result[x].replace(']', '}')
    return result

def getInterfaces():
    return [x for x in os.listdir('/sys/class/net') if any(y in x for y in ['wl','eth','enp'])]

theme = getTheme(THEME_PATH)
poly_theme = {}
poly_theme['poly_wlan'] = poly_theme['poly_lan1'] = ""
poly_theme['poly_lan2'] = ""
for i in getInterfaces():
    if 'w' in i:
        poly_theme['poly_wlan'] = i
    elif not poly_theme['poly_lan1']:
        poly_theme['poly_lan1'] = i
    else:
        poly_theme['poly_lan2'] = i
poly_theme['ewmhactive'] = f'%[B{theme["background"]}]%[F{theme["focusedbg"]}]{theme["leftmoduleprefix"]}%[F-]%[B-]%[B{theme["focusedbg"]}]%[F{theme["focusedfg"]}]{" "*theme["wspadding"]}%index% %icon%{" "*theme["wspadding"]}%[F-]%[B-]%[B{theme["background"]}]%[F{theme["focusedbg"]}]{theme["leftmodulesuffix"]}%[F-]%[B-]'
# power menu widgets
poly_theme['poweropen']= '%[B{}]%[F{}]{}%[F-]%[B-]%[B{}]%[F{}]{}{}{}%[F-]%[B-]%[B{}]%[F{}]{}%[F-]%[B-]'.format(theme['background'],
        theme['titlebg'],theme['rightmoduleprefix'],theme['titlebg'],theme['titlefg'],
        " "*theme['titlepadding'],POWER_ICONS['power']," "*theme['titlepadding'],theme['background'],
        theme['titlebg'],theme['rightmodulesuffix'])
poly_theme['powerclose']= '%[B{}]%[F{}]{}%[F-]%[B-]%[B{}]%[F{}]{}{}%[F-]%[B-]%[B{}]%[F{}]{}%[F-]%[B-]'.format(theme['background'],
        theme['titlebg'],theme['rightmoduleprefix'],theme['titlebg'],theme['titlefg'],
        " "*theme['titlepadding']," "*theme['titlepadding'],theme['background'],
        theme['titlebg'],theme['rightmodulesuffix'])
poly_theme['power00']= '%[B{}]%[F{}]{}%[F-]%[B-]%[B{}]%[F{}]{}{}{}%[F-]%[B-]%[B{}]%[F{}]{}%[F-]%[B-]'.format(theme['background'],
        theme['titlebg'],theme['rightmoduleprefix'],theme['titlebg'],theme['titlefg'],
        " "*theme['bodypadding'],POWER_ICONS['reboot']," "*theme['bodypadding'],theme['background'],
        theme['titlebg'],theme['rightmodulesuffix'])
poly_theme['power01']= '%[B{}]%[F{}]{}%[F-]%[B-]%[B{}]%[F{}]{}{}{}%[F-]%[B-]%[B{}]%[F{}]{}%[F-]%[B-]'.format(theme['background'],
        theme['titlebg'],theme['rightmoduleprefix'],theme['titlebg'],theme['titlefg'],
        " "*theme['bodypadding'],POWER_ICONS['power']," "*theme['bodypadding'],theme['background'],
        theme['titlebg'],theme['rightmodulesuffix'])
poly_theme['power02']= '%[B{}]%[F{}]{}%[F-]%[B-]%[B{}]%[F{}]{}{}{}%[F-]%[B-]%[B{}]%[F{}]{}%[F-]%[B-]'.format(theme['background'],
        theme['titlebg'],theme['rightmoduleprefix'],theme['titlebg'],theme['titlefg'],
        " "*theme['bodypadding'],POWER_ICONS['logout']," "*theme['bodypadding'],theme['background'],
        theme['titlebg'],theme['rightmodulesuffix'])
poly_theme['power03']= '%[B{}]%[F{}]{}%[F-]%[B-]%[B{}]%[F{}]{}{}{}%[F-]%[B-]%[B{}]%[F{}]{}%[F-]%[B-]'.format(theme['background'],
        theme['titlebg'],theme['rightmoduleprefix'],theme['titlebg'],theme['titlefg'],
        " "*theme['bodypadding'],POWER_ICONS['lock']," "*theme['bodypadding'],theme['background'],
        theme['titlebg'],theme['rightmodulesuffix'])
poly_theme['power10']= '%[B{}]%[F{}]{}%[F-]%[B-]%[B{}]%[F{}]{}{}{}%[F-]%[B-]%[B{}]%[F{}]{}%[F-]%[B-]'.format(theme['background'],
        theme['titlebg'],theme['rightmoduleprefix'],theme['titlebg'],theme['titlefg'],
        " "*theme['bodypadding'],POWER_ICONS['reboot']," "*theme['bodypadding'],theme['background'],
        theme['titlebg'],theme['rightmodulesuffix'])
poly_theme['power20']= '%[B{}]%[F{}]{}%[F-]%[B-]%[B{}]%[F{}]{}{}{}%[F-]%[B-]%[B{}]%[F{}]{}%[F-]%[B-]'.format(theme['background'],
        theme['titlebg'],theme['rightmoduleprefix'],theme['titlebg'],theme['titlefg'],
        " "*theme['bodypadding'],POWER_ICONS['power']," "*theme['bodypadding'],theme['background'],
        theme['titlebg'],theme['rightmodulesuffix'])
poly_theme['power30']= '%[B{}]%[F{}]{}%[F-]%[B-]%[B{}]%[F{}]{}{}{}%[F-]%[B-]%[B{}]%[F{}]{}%[F-]%[B-]'.format(theme['background'],
        theme['titlebg'],theme['rightmoduleprefix'],theme['titlebg'],theme['titlefg'],
        " "*theme['bodypadding'],POWER_ICONS['logout']," "*theme['bodypadding'],theme['background'],
        theme['titlebg'],theme['rightmodulesuffix'])
for i in poly_theme:
    poly_theme[i] = poly_theme[i].replace('[','{')
    poly_theme[i] = poly_theme[i].replace(']','}')
poly_screens = {}
for i, monitor in enumerate(MONITORS):
    os.environ['POLY_MONITOR'] = monitor
    os.environ['POLY_WS_FIFO_PATH'] = f'tail -F /tmp/qtile_ws_{i}'
    os.environ['POLY_WS_FIFO_CHECK'] = f'[ -p /tmp/qtile_ws_{i} ]'
    os.environ['POLY_EWMHACTIVE'] = poly_theme['ewmhactive']
    os.environ['POLY_THEME_PATH'] = THEME_PATH
    os.environ['POLY_POWER_OPEN'] = poly_theme['poweropen']
    os.environ['POLY_POWER_CLOSE'] = poly_theme['powerclose']
    os.environ['POLY_POWER_0-0'] = poly_theme['power00']
    os.environ['POLY_POWER_0-1'] = poly_theme['power01']
    os.environ['POLY_POWER_0-2'] = poly_theme['power02']
    os.environ['POLY_POWER_0-3'] = poly_theme['power03']
    os.environ['POLY_POWER_1-0'] = poly_theme['power10']
    os.environ['POLY_POWER_2-0'] = poly_theme['power20']
    os.environ['POLY_POWER_3-0'] = poly_theme['power30']
    os.environ['POLY_WLAN'] = poly_theme['poly_wlan']
    os.environ['POLY_LAN1'] = poly_theme['poly_lan1']
    os.environ['POLY_LAN2'] = poly_theme['poly_lan2']
    try:
        subprocess.run(['killall', '-q', 'polybar'])
        o = subprocess.Popen('polybar -r island', shell=True)
        poly_screens[i] = {'name':monitor, 'pid':o.pid, 
                'ws_fifo_path':f'/tmp/qtile_ws_{i}', 'ws_format':'', 'layout_format':''}
    except subprocess.CalledProcessError as e:
        logger.warn(e.output.decode().strip())
print(poly_theme)
print(poly_screens)
print(os.getenv('POLY_POWER_0-0'))
