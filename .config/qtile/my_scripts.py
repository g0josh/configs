import subprocess
import time
from datetime import datetime, timedelta
import re
import os
from contextlib import contextmanager
import json
import yaml
import my_audio as audio

from libqtile.log_utils import logger
from libqtile.command import lazy
from socket import error as socket_error

POWER_ICONS = {'power': '', 'reboot': '', 'lock': '', 'logout': ''}
LAYOUT_ICONS = {'columns': 'HHH', 'monadtall': '[]=',
                'monadwide': 'TTT', 'max': '[ ]', 'treetab': '|[]'}
MOUSE_BUTTONS = {'LEFT_CLICK': 1, 'RIGHT_CLICK': 2,
                 'SCROLL_UP': 4, 'SCROLL_DOWN': 5}
POWER_BUTTONS = {'SHUT_DOWN': 0, 'LOG_OUT': 1, 'LOCK_SCREEN': 2}
THEME = {}


# ---------------------------------------------
# Group
# ---------------------------------------------
def getGroupLabel(qtile, group, x=0, y=0, button=1):
    for _group in qtile.groups:
        if group == _group.name:
            return _group.label if (_group.screen is not None or len(_group.windows) > 0) else False
    return False

def getGroupColors(qtile, group, theme, screen=0):
    curr_group = qtile.current_group.name
    curr_screen = qtile.current_group.screen.index
    if curr_group == group and curr_screen == screen :
        return {'foreground': theme['focusedfg'], 'background': theme['focusedbg']}
    curr_screen = qtile.current_group.screen.index
    for _group in qtile.groups:
        if group == _group.name:
            if _group.screen is None:
                return {'foreground': theme['bodyfg'], 'background': theme['bodybg']}
            elif _group.screen.index == screen:
                return {'foreground': theme['altfg'], 'background': theme['altbg']}
            break
    return {'foreground': theme['bodyfg'], 'background': theme['bodybg']}

# ---------------------------------------------
# VOLUME
# ---------------------------------------------

def volumePressed(button, x=0, y=0, qtile=None):
    if button in [MOUSE_BUTTONS['LEFT_CLICK'], MOUSE_BUTTONS['RIGHT_CLICK']]:
        audio.setMute(2)
    elif button == MOUSE_BUTTONS['SCROLL_UP']:
        audio.setVolume("+5%")
    elif button == MOUSE_BUTTONS['SCROLL_DOWN']:
        audio.setVolume("-5%")
    else:
        logger.warning('Uknown mouse click = {}'.format(button))


def getVolumeIcon(muted_icon='', icons=['', '', ''], volume=None, qtile=None):
    # check if muted
    if audio.isMuted() == True:
        return muted_icon

    # Check volume level
    if volume is None:
        volume = audio.getVolume()

    margin = 100 / len(icons)
    index, _ = divmod(volume, margin)
    if index >= len(icons):
        index = len(icons) - 1
    return icons[int(index)]


def getVolume(qtile=None):
    if audio.isMuted() == True:
        return ""
    return audio.getVolume()

# ---------------------------------------------
# MPD
# ---------------------------------------------

def getCmus(not_connected_text='', max_title_len=20, qtile=None):
    try:
        output = subprocess.check_output(['cmus-remote', '-Q']).decode()
    except subprocess.CalledProcessError as e:
        logger.warn("getMpd: {}".format(e))
        return not_connected_text
    else:
        output = re.findall(r'file (.*)|duration (\d+)|position (\d+)|tag title (.*)', output, re.MULTILINE)

    try:
        if len(output) > 3:
            title = output[3][-1].strip()
        else:
            title = output[0][0].split('/')[-1].split('.')[0].strip()
        title = title[:max_title_len-3] + '...' if len(title) > max_title_len else "{}{}".format(
            title, " "*(max_title_len-len(title)))
        total_time_m = int(output[1][1])//60
        total_time_s = int(output[1][1])%60
        time_m = int(output[2][2])//60
        time_s = int(output[2][2])%60

    except Exception as e:
        logger.warning("{} {}".format(e, output))
        return not_connected_text
    else:
        return "{} {}:{}/{}:{}".format(title, time_m, time_s, total_time_m, total_time_s)

def clickCmus(button, x=0, y=0, qtile=None):
    keys = {
        # Left mouse button
        "toggle": 1,
        # Right mouse button
        "stop": 3,
        # Scroll up
        "previous": 4,
        # Scroll down
        "next": 5,
        # User defined command
        "command": None
    }
    cmd = ['cmus-remote']
    if button == keys["toggle"]:
        cmd.append('--pause')
    elif button == keys["stop"]:
        cmd.append('--stop')
    elif button == keys["previous"]:
        cmd.append('--prev')
    elif button == keys["next"]:
        cmd.append('--next')
    try:
        subprocess.run(cmd)
    except subprocess.CalledProcessError as e:
        logger.warning(e.output.decode().strip())

def getMpd(not_connected_text='', max_title_len=20, qtile=None):
    try:
        output = subprocess.check_output(['mpc']).decode()
    except subprocess.CalledProcessError as e:
        # logger.warn("getMpd: {}".format(e))
        return not_connected_text
    else:
        output = output.split('\n')
    try:
        title = output[0].split('-')[-1].strip()
        title = title[:12] + '...' if len(title) > max_title_len else "{}{}".format(
            title, " "*(max_title_len-len(title)))
        time = output[1].split()[-2]
    except Exception as e:
        # logger.warning(e)
        return not_connected_text
    else:
        return "{} - {}".format(title, time)


def clickMpd(button, x=0, y=0, qtile=None):
    keys = {
        # Left mouse button
        "toggle": 1,
        # Right mouse button
        "stop": 3,
        # Scroll up
        "previous": 4,
        # Scroll down
        "next": 5,
        # User defined command
        "command": None
    }
    cmd = ['mpc']
    if button == keys["toggle"]:
        cmd.append('toggle')
    elif button == keys["stop"]:
        cmd.append('stop')
    elif button == keys["previous"]:
        cmd.append('prev')
    elif button == keys["next"]:
        cmd.append('next')
    try:
        subprocess.run(cmd)
    except subprocess.CalledProcessError as e:
        logger.warning(e.output.decode().strip())

# ---------------------------------------------
# Internet
# ---------------------------------------------


net_speed_objects = []


class NetSpeeds(object):
    def __init__(self, interface="wlp2s0"):
        self.init_time = 0
        self.init_bytes_tx_rx = [0, 0]
        self.interface = interface

    def getSpeed(self):
        bytes_tx_rx = []
        for f in ['/sys/class/net/{}/statistics/tx_bytes'.format(self.interface),
                  '/sys/class/net/{}/statistics/rx_bytes'.format(self.interface)]:
            with open(f, 'r') as fo:
                bytes_tx_rx.append(int(fo.read()))
        _time = time.time()
        speeds = [(x - y) / (_time - self.init_time)
                  for x, y in zip(bytes_tx_rx, self.init_bytes_tx_rx)]
        self.init_bytes_tx_rx = bytes_tx_rx
        self.init_time = _time
        speeds = ["{:3.0f} kB/s".format(x/1e3) if x <
                  1e6 else "{:2.1f} MB/s".format(x/1e6) for x in speeds]
        return {'upload': speeds[0], 'download': speeds[1]}


def getInterfaces():
    return [x for x in os.listdir('/sys/class/net') if any(y in x for y in ['wl', 'eth', 'enp'])]


def getWlan(interface='wlo1', widgets=[], ontexts=[], offtexts=[], error_text='', qtile=None):
    try:
        output = subprocess.check_output(['nmcli']).decode()
    except subprocess.CalledProcessError as e:
        logger.warning(e.output.decode().strip())
        return error_text
    else:
        _essid = re.search(f'{interface}:\s+connected\s+\w+\s+(\S+)\n', output)

    if not _essid:
        return ""
    essid = _essid.group(1)

    # get speeds
    global net_speed_objects
    speed_obj = None
    for o in net_speed_objects:
        if o.interface == interface:
            speed_obj = o

    if speed_obj is None:
        speed_obj = NetSpeeds(interface=interface)
        net_speed_objects.append(speed_obj)

    try:
        speed = speed_obj.getSpeed()['download']
    except Exception as e:
        logger.warning(e)
        return "  0 kb/s"
    else:
        return "{}|{}".format(essid, speed)


def getLan(interface='enp24s0', error_text='', qtile=None):
    # check if enabled:
    up = []
    for _file in ['/sys/class/net/{}/operstate'.format(interface),
                  '/sys/class/net/{}/carrier'.format(interface)]:
        if not os.path.exists(_file):
            return error_text
        try:
            with open(_file, 'r') as f:
                up.append(f.read().strip().lower())
        except:
            up.append("-1")
    if up != ['up', '1']:
        return ""

    # get speeds
    global net_speed_objects
    speed_obj = None
    for o in net_speed_objects:
        if o.interface == interface:
            speed_obj = o

    if speed_obj is None:
        speed_obj = NetSpeeds(interface=interface)
        net_speed_objects.append(speed_obj)

    try:
        speed = speed_obj.getSpeed()['download']
    except Exception as e:
        logger.warning(e)
        return "  0 kb/s"
    else:
        return speed

# ---------------------------------------------
# MISC
# ---------------------------------------------

# Setting a time zone


@contextmanager
def setTimeZone(the_tz):
    orig = os.environ.get('TZ')
    os.environ['TZ'] = the_tz
    time.tzset()
    yield
    if orig is not None:
        os.environ['TZ'] = orig
    else:
        del os.environ['TZ']
    time.tzset()


def getTime(format='%b %d, %A, %I:%M %p', timezone=None, qtile=None):
    def _get_time():
        now = datetime.now().astimezone()
        return (now + timedelta(seconds=0.5)).strftime(format)

    if timezone is not None:
        with setTimeZone(timezone):
            return _get_time()
    else:
        return _get_time()


def getlocksStatus(qtile=None):
    result = []
    try:
        output = subprocess.check_output(['xset', 'q']).decode()
        output = re.findall(r"(Caps|Num)\s+Lock:\s*(\w*)", output)
    except subprocess.CalledProcessError as e:
        logger.warning(e.output.decode().strip())
        return ""

    if ('Caps', 'on') in output:
        result.append('A')
    if ('Num', 'on') in output:
        result.append('0')
    return " ".join(result)


def getTemps(x=0, y=0, button=1, threshold=40, qtile=None):
    try:
        cpu = subprocess.check_output(['sensors']).decode().strip()
        gpu = subprocess.check_output(['nvidia-smi']).decode().strip()
    except subprocess.CalledProcessError as e:
        logger.warning(e.output.decode().strip())
        return 'error'

    _cpu_temp = re.search(r'\d+\.\d+°C', cpu, flags=re.UNICODE)
    _gpu_temp = re.search(r'\s\d+C\s', gpu)
    cpu_temp = gpu_temp = 0
    if _cpu_temp:
        cpu_temp = _cpu_temp.group()[:-4]
    if _gpu_temp:
        gpu_temp = _gpu_temp.group().strip()[:-1]

    if int(cpu_temp) > threshold or int(gpu_temp) > threshold:
        return '{}|{}'.format(cpu_temp, gpu_temp)


def getUtilization(x=0, y=0, button=1, threshold=10, qtile=None):
    try:
        cpu = subprocess.check_output(['top', '-bn2', '-d0.1']).decode()
        gpu = subprocess.check_output(
            ['nvidia-smi', '-q', '-d', 'UTILIZATION']).decode()
    except subprocess.CalledProcessError as e:
        logger.warning(e.output.decode().strip())
        return 'error'

    _cpu_util = re.search(r'load average:\s(\d+\.\d+)', cpu)
    _gpu_util = re.search(r'Gpu\s+:\s\d+', gpu)
    cpu_util = gpu_util = 0
    if _cpu_util:
        u = _cpu_util.group().split(':')[-1].strip()
        cpu_util = '{:0.0f}'.format(float(u) * 100 / os.cpu_count())
    if _gpu_util:
        gpu_util = _gpu_util.group().split(':')[-1].strip()

    if int(cpu_util) > threshold or int(gpu_util) > threshold:
        return "{}|{}".format(cpu_util, gpu_util)


def powerClicked(button, power_button, x=0, y=0, qtile=None):
    if button != MOUSE_BUTTONS['LEFT_CLICK']:
        return

    if power_button == POWER_BUTTONS['SHUT_DOWN']:
        cmd = ['shutdown', 'now']
    elif power_button == POWER_BUTTONS['LOG_OUT']:
        cmd = ['qtile-cmd', '-o', 'cmd', '-f', 'shutdown']
    elif power_button == POWER_BUTTONS['LOCK_SCREEN']:
        cmd = [os.path.expanduser("~/.config/qtile/lockscreen.sh")]

    if cmd:
        try:
            subprocess.run(cmd)
        except subprocess.CalledProcessError as e:
            logger.warning(e.output.decode().strip())


def getNumScreens():
    try:
        o = subprocess.check_output(['xrandr']).decode()
    except subprocess.CalledProcessError as e:
        logger.warning(e.output.decode().strip())
        return 1
    else:
        return len(re.findall(r'\w+ connected \w+', o))


def getTheme(path):
    global THEME
    with open(path, 'r') as fh:
        theme = yaml.safe_load(fh)
    THEME = theme
    return theme

def setupMonitors():
    try:
        o = subprocess.check_output(['xrandr']).decode()
    except subprocess.CalledProcessError as e:
        logger.warning(e.output.decode().strip())
        return

    cmd = ["xrandr"]
    x = 0
    monitors = []
    for i, e in enumerate(o.split('\n')):
        if not 'connected' in e:
            continue

        name = e.strip().split()[0]
        if ' connected' in e:
            res = o.split('\n')[i+1].strip().split()[0]
            cmd += ['--output', name, '--mode', res,
                    '--pos', "{}x{}".format(x, 0), '--rotate', 'normal']
            x += int(res.split('x')[0])
            monitors.append(name)
        elif 'disconnected' in e:
            cmd += ['--output', name, '--off']

    try:
        subprocess.run(cmd)
    except subprocess.CalledProcessError as e:
        logger.warning(e.output.decode().strip())
    else:
        return monitors


def startPolybar(theme_path):
    monitors = setupMonitors()
    theme = getTheme(theme_path)
    os.environ['POLY_WLAN'] = os.environ['POLY_LAN1'] = ""
    os.environ['POLY_LAN2'] = ""
    for i in getInterfaces():
        if 'w' in i:
            os.environ['POLY_WLAN'] = i
        elif not os.getenv('POLY_LAN1'):
            os.environ['POLY_LAN1'] = i
        else:
            os.environ['POLY_LAN2'] = i
    poly_theme = {}
    poly_theme['ewmhactive'] = f'%[B{theme["background"]}]%[F{theme["focusedbg"]}]{theme["leftmoduleprefix"]}%[F-]%[B-]%[B{theme["focusedbg"]}]%[F{theme["focusedfg"]}]{" "*theme["wspadding"]}%index% %icon%{" "*theme["wspadding"]}%[F-]%[B-]%[B{theme["background"]}]%[F{theme["focusedbg"]}]{theme["leftmodulesuffix"]}%[F-]%[B-]'
    # power menu widgets
    poly_theme['poweropen'] = '%[B{}]%[F{}]{}%[F-]%[B-]%[B{}]%[F{}]{}{}{}%[F-]%[B-]%[B{}]%[F{}]{}%[F-]%[B-]'.format(theme['background'],
                                                                                                                    theme['titlebg'], theme['rightmoduleprefix'], theme[
                                                                                                                        'titlebg'], theme['titlefg'],
                                                                                                                    " " *
                                                                                                                    theme['titlepadding'], POWER_ICONS[
                                                                                                                        'power'], " "*theme['titlepadding'], theme['background'],
                                                                                                                    theme['titlebg'], theme['rightmodulesuffix'])
    poly_theme['powerclose'] = '%[B{}]%[F{}]{}%[F-]%[B-]%[B{}]%[F{}]{}{}%[F-]%[B-]%[B{}]%[F{}]{}%[F-]%[B-]'.format(theme['background'],
                                                                                                                    theme['titlebg'], theme['rightmoduleprefix'], theme[
                                                                                                                        'titlebg'], theme['titlefg'],
                                                                                                                    " "*theme['titlepadding'], " " *
                                                                                                                    theme['titlepadding'], theme[
                                                                                                                        'background'],
                                                                                                                    theme['titlebg'], theme['rightmodulesuffix'])
    poly_theme['power00'] = '%[B{}]%[F{}]{}%[F-]%[B-]%[B{}]%[F{}]{}{}{}%[F-]%[B-]%[B{}]%[F{}]{}%[F-]%[B-]'.format(theme['background'],
                                                                                                                  theme['titlebg'], theme['rightmoduleprefix'], theme[
                                                                                                                      'titlebg'], theme['titlefg'],
                                                                                                                  " " *
                                                                                                                  theme['bodypadding'], POWER_ICONS[
                                                                                                                      'reboot'], " "*theme['bodypadding'], theme['background'],
                                                                                                                  theme['titlebg'], theme['rightmodulesuffix'])
    poly_theme['power01'] = '%[B{}]%[F{}]{}%[F-]%[B-]%[B{}]%[F{}]{}{}{}%[F-]%[B-]%[B{}]%[F{}]{}%[F-]%[B-]'.format(theme['background'],
                                                                                                                  theme['titlebg'], theme['rightmoduleprefix'], theme[
                                                                                                                      'titlebg'], theme['titlefg'],
                                                                                                                  " " *
                                                                                                                  theme['bodypadding'], POWER_ICONS[
                                                                                                                      'power'], " "*theme['bodypadding'], theme['background'],
                                                                                                                  theme['titlebg'], theme['rightmodulesuffix'])
    poly_theme['power02'] = '%[B{}]%[F{}]{}%[F-]%[B-]%[B{}]%[F{}]{}{}{}%[F-]%[B-]%[B{}]%[F{}]{}%[F-]%[B-]'.format(theme['background'],
                                                                                                                  theme['titlebg'], theme['rightmoduleprefix'], theme[
                                                                                                                      'titlebg'], theme['titlefg'],
                                                                                                                  " " *
                                                                                                                  theme['bodypadding'], POWER_ICONS[
                                                                                                                      'logout'], " "*theme['bodypadding'], theme['background'],
                                                                                                                  theme['titlebg'], theme['rightmodulesuffix'])
    poly_theme['power03'] = '%[B{}]%[F{}]{}%[F-]%[B-]%[B{}]%[F{}]{}{}{}%[F-]%[B-]%[B{}]%[F{}]{}%[F-]%[B-]'.format(theme['background'],
                                                                                                                  theme['titlebg'], theme['rightmoduleprefix'], theme[
                                                                                                                      'titlebg'], theme['titlefg'],
                                                                                                                  " " *
                                                                                                                  theme['bodypadding'], POWER_ICONS[
                                                                                                                      'lock'], " "*theme['bodypadding'], theme['background'],
                                                                                                                  theme['titlebg'], theme['rightmodulesuffix'])
    poly_theme['power10'] = '%[B{}]%[F{}]{}%[F-]%[B-]%[B{}]%[F{}]{}{}{}%[F-]%[B-]%[B{}]%[F{}]{}%[F-]%[B-]'.format(theme['background'],
                                                                                                                  theme['titlebg'], theme['rightmoduleprefix'], theme[
                                                                                                                      'titlebg'], theme['titlefg'],
                                                                                                                  " " *
                                                                                                                  theme['bodypadding'], POWER_ICONS[
                                                                                                                      'reboot'], " "*theme['bodypadding'], theme['background'],
                                                                                                                  theme['titlebg'], theme['rightmodulesuffix'])
    poly_theme['power20'] = '%[B{}]%[F{}]{}%[F-]%[B-]%[B{}]%[F{}]{}{}{}%[F-]%[B-]%[B{}]%[F{}]{}%[F-]%[B-]'.format(theme['background'],
                                                                                                                  theme['titlebg'], theme['rightmoduleprefix'], theme[
                                                                                                                      'titlebg'], theme['titlefg'],
                                                                                                                  " " *
                                                                                                                  theme['bodypadding'], POWER_ICONS[
                                                                                                                      'power'], " "*theme['bodypadding'], theme['background'],
                                                                                                                  theme['titlebg'], theme['rightmodulesuffix'])
    poly_theme['power30'] = '%[B{}]%[F{}]{}%[F-]%[B-]%[B{}]%[F{}]{}{}{}%[F-]%[B-]%[B{}]%[F{}]{}%[F-]%[B-]'.format(theme['background'],
                                                                                                                  theme['titlebg'], theme['rightmoduleprefix'], theme[
                                                                                                                      'titlebg'], theme['titlefg'],
                                                                                                                  " " *
                                                                                                                  theme['bodypadding'], POWER_ICONS[
                                                                                                                      'logout'], " "*theme['bodypadding'], theme['background'],
                                                                                                                  theme['titlebg'], theme['rightmodulesuffix'])
    for i in poly_theme:
        poly_theme[i] = poly_theme[i].replace('[', '{')
        poly_theme[i] = poly_theme[i].replace(']', '}')
    poly_screens = {}
    for i, monitor in enumerate(monitors):
        os.environ['POLY_MONITOR'] = monitor
        os.environ['POLY_WS_FIFO_PATH'] = f'tail -F /tmp/qtile_ws_{i}'
        os.environ['POLY_WS_FIFO_CHECK'] = f'[ -p /tmp/qtile_ws_{i} ]'
        os.environ['POLY_EWMHACTIVE'] = poly_theme['ewmhactive']
        os.environ['POLY_THEME_PATH'] = theme_path
        os.environ['POLY_POWER_OPEN'] = poly_theme['poweropen']
        os.environ['POLY_POWER_CLOSE'] = poly_theme['powerclose']
        os.environ['POLY_POWER_0-0'] = poly_theme['power00']
        os.environ['POLY_POWER_0-1'] = poly_theme['power01']
        os.environ['POLY_POWER_0-2'] = poly_theme['power02']
        os.environ['POLY_POWER_0-3'] = poly_theme['power03']
        os.environ['POLY_POWER_1-0'] = poly_theme['power10']
        os.environ['POLY_POWER_2-0'] = poly_theme['power20']
        os.environ['POLY_POWER_3-0'] = poly_theme['power30']
        try:
            subprocess.run(['killall', '-q', 'polybar'])
            o = subprocess.Popen('polybar -r island', shell=True)
            poly_screens[i] = {'name': monitor, 'pid': o.pid,
                               'ws_fifo_path': f'/tmp/qtile_ws_{i}', 'ws_format': '', 'layout_format': ''}
        except subprocess.CalledProcessError as e:
            logger.warn(e.output.decode().strip())
    logger.warn(poly_screens)
    return poly_screens


def updateWallpaper(qtile, adjustWindowCount=0):
    groups = qtile.cmd_groups()
    windows = adjustWindowCount
    for group in groups:
        if groups[group]["screen"] is None:
            continue
        windows += len(groups[group]["windows"])

    wall = "BlurredWallpaper" if windows > 0 else "Wallpaper"
    wallPath = os.path.expanduser("~/Pictures/") + wall
    cmd = "feh --bg-fill " + wallPath
    p = subprocess.Popen(cmd.split())
    #p = subprocess.Popen(cmd.split(), stderr=subprocess.PIPE, stdout=subprocess.PIPE)
    #stdout, stderr = p.communicate()
    # if stdout or stderr:
    #    logger.warning("out = {}, err = {}".format(stdout , stderr))
