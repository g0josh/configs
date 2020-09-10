import subprocess
import time
from datetime import datetime, timedelta
import re
import os
from contextlib import contextmanager
import json
import yaml
from typing import Optional, List

from libqtile.log_utils import logger
from libqtile.command import lazy
from libqtile.core.manager import Qtile
from socket import error as socket_error

import my_audio as audio
from my_widgets import ComboWidgetColor
from icons import getIcons

MOUSE_BUTTONS = {'LEFT_CLICK': 1, 'RIGHT_CLICK': 2,
                 'SCROLL_UP': 4, 'SCROLL_DOWN': 5}
POWER_BUTTONS = {'SHUT_DOWN': 0, 'LOG_OUT': 1, 'LOCK_SCREEN': 2}
THEME = {}


# ---------------------------------------------
# Group
# ---------------------------------------------

def getGroupLabel(qtile:Qtile, group:str):
    for _group in qtile.groups:
        if group == _group.name:
            return _group.label if (_group.screen is not None or len(_group.windows) > 0) else ""
    return ""

def getGroupColors(qtile:Qtile, group:str, theme:dict, screen:int=0) -> ComboWidgetColor:
    curr_group = qtile.current_group.name
    curr_screen = qtile.current_group.screen.index
    if curr_group == group and curr_screen == screen :
        return ComboWidgetColor(foreground=theme['focusedfg'],background=theme['focusedbg'])
    curr_screen = qtile.current_group.screen.index
    for _group in qtile.groups:
        if group == _group.name:
            if _group.screen is None:
                return ComboWidgetColor(foreground=theme['bodyfg'],background=theme['bodybg'])
            elif _group.screen.index == screen:
                return ComboWidgetColor(foreground=theme['altfg'],background=theme['altbg'])
            break
    return ComboWidgetColor(foreground=theme['bodyfg'],background=theme['bodybg'])


# ---------------------------------------------
# BATTERY
# ---------------------------------------------

def getBatteryStatusIcon(qtile:Qtile=None):
    try:
        with open("/sys/class/power_supply/BAT0/status") as sf:
            status = sf.read()
    except:
        return ""

    if "Charging" in status:
        return ""

    try:
        index = min( int(getBatteryCapacity()[:-1])//25, 3)
    except:
        index = 0

    return getIcons()['battery'][index]
    
def getBatteryCapacity(qtile:Qtile=None):
    try:
        with open("/sys/class/power_supply/BAT0/capacity") as cf:
            capacity = cf.read().strip()
    except:
        return 0

    return f'{capacity}%'

# ---------------------------------------------
# VOLUME
# ---------------------------------------------

def volumeClicked(qtile:Qtile, button:int):
    if button in [MOUSE_BUTTONS['LEFT_CLICK'], MOUSE_BUTTONS['RIGHT_CLICK']]:
        audio.setMute(2)
    elif button == MOUSE_BUTTONS['SCROLL_UP']:
        audio.setVolume("+5%")
    elif button == MOUSE_BUTTONS['SCROLL_DOWN']:
        audio.setVolume("-5%")
    else:
        logger.warning('Uknown mouse click = {}'.format(button))

def getVolumeIcon(qtile:Qtile):
    # check if muted
    if audio.isMuted() == True:
        return getIcons()['mute']

    # Check volume level
    volume = audio.getVolume()
    icons = getIcons()['volume']
    margin = 100 / len(icons)
    index, _ = divmod(volume, margin)
    if index >= len(icons):
        index = len(icons) - 1
    return icons[int(index)]

def getVolume(qtile:Qtile):
    if audio.isMuted() == True:
        return ""
    return audio.getVolume()

# ---------------------------------------------
# Music
# ---------------------------------------------

def getCmus(qtile:Optional[Qtile]=None, max_title_len:int=20):
    try:
        output = subprocess.check_output(['cmus-remote', '-Q']).decode()
    except subprocess.CalledProcessError as e:
        logger.warn("getMpd: {}".format(e))
        return getIcons()['error']
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
        return getIcons()['error']
    else:
        return "{} {}:{}/{}:{}".format(title, time_m, time_s, total_time_m, total_time_s)

def clickCmus(qtile:Optional[Qtile]=None, button:int=1):
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

def getMpd( qtile:Optional[Qtile]=None, not_connected_text:str='', max_title_len:int=20):
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

def clickMpd(qtile:Optional[Qtile]=None, button:int=1):
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
        self.prev_speeds = [0, 0]

    def formatSpeeds(self):
        return {'upload': self.prev_speeds[0], 'download': self.prev_speeds[1]}

    def getSpeed(self):
        if time.time() - self.init_time < 5:
            return self.formatSpeeds()

        bytes_tx_rx = []
        for f in ['/sys/class/net/{}/statistics/tx_bytes'.format(self.interface),
                  '/sys/class/net/{}/statistics/rx_bytes'.format(self.interface)]:
            with open(f, 'r') as fo:
                bytes_tx_rx.append(int(fo.read()))
        _time = time.time()
        self.prev_speeds = [(x - y) / (_time - self.init_time)
                  for x, y in zip(bytes_tx_rx, self.init_bytes_tx_rx)]
        self.init_bytes_tx_rx = bytes_tx_rx
        self.init_time = _time
        return self.formatSpeeds()

def getNetSpeeds(interface:str="wlo1", show_speed_above:int=1e3):
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
        speeds = speed_obj.getSpeed()
    except Exception as e:
        logger.warn("getNetSpeeds error: {}".format(e))

    def format_speed(speed:int):
        return "{:3.0f} kB/s".format(speed/1e3) if speed < 1e6 else "{:2.1f} MB/s".format(speed/1e6)

    for k in speeds:
        speeds[k] = format_speed(speeds[k]) if speeds[k] > show_speed_above else ""

    return speeds

# def getNetSpeed(qtile:Optional[Qtile]=None, interface:str="wlo1", upload=False, min=10e3):
#     # get speeds
#     global net_speed_objects
#     speed_obj = None
#     for o in net_speed_objects:
#         if o.interface == interface:
#             speed_obj = o

#     if speed_obj is None:
#         speed_obj = NetSpeeds(interface=interface)
#         net_speed_objects.append(speed_obj)

#     try:
#         speed = speed_obj.getSpeed()
#     except Exception as e:
#         logger.warn("getNetSpeed error: {}".format(e))

#     speed = speed["upload"] if upload else speed["download"]
#     if speed < min:
#         return ""
#     else:
#         return "{:3.0f} kB/s".format(speed/1e3) if speed < 1e6 else "{:2.1f} MB/s".format(speed/1e6)
    
def getInterfaces():
    return [x for x in os.listdir('/sys/class/net') if any(y in x for y in ['wl', 'eth', 'enp'])]

def getWlan(qtile:Optional[Qtile]=None, interface:str='wlo1', error_text:str='', show_speed_above:int=10e3):
    try:
        output = subprocess.check_output(['nmcli']).decode()
    except subprocess.CalledProcessError as e:
        logger.warning(e.output.decode().strip())
        return error_text
    else:
        _essid = re.search(f'{interface}:\s+connected\s+\w+\s+(\S+)\n', output)

    if not _essid:
        return ""
    
    speeds = getNetSpeeds(interface, show_speed_above)
    result = _essid.group(1)
    result = result + " {} {}".format(getIcons()['download'], speeds['download']) if speeds['download'] else result
    result = result + " {} {}".format(getIcons()['upload'], speeds['upload']) if speeds['upload'] else result
    return result

def getLan(qtile:Optional[Qtile]=None, interface:str='enp24s0', error_text:str='', show_speed_above:int=10e3):
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
    else:
        speeds = getNetSpeeds(interface, show_speed_above)
        result = "{} {}".format(getIcons()['download'], speeds['download']) if speeds['download'] else ""
        result = result + " {} {}".format(getIcons()['upload'], speeds['upload']) if speeds['upload'] else result
        return result

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

def getTime(qtile:Optional[Qtile]=None, format:str='%b %d, %A, %I:%M %p', timezone:Optional[str]=None):
    def _get_time():
        now = datetime.now().astimezone()
        return (now + timedelta(seconds=0.5)).strftime(format)

    if timezone is not None:
        with setTimeZone(timezone):
            return _get_time()
    else:
        return _get_time()

def getlocksStatus(qtile:Optional[Qtile]=None):
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

def getTemps(qtile:Optional[Qtile]=None, threshold:int=-1 ):
    try:
        cpu = subprocess.check_output(['sensors']).decode().strip()
    except:
        cpu = ""
    try:
        gpu = subprocess.check_output(['nvidia-smi']).decode().strip()
    except:
        gpu = ""
    
    _cpu_temp = re.search(r'\d+\.\d+°C', cpu, flags=re.UNICODE) if cpu else None
    _gpu_temp = re.search(r'\s\d+C\s', gpu) if gpu else None
    cpu_temp = gpu_temp = 0
    if _cpu_temp:
        cpu_temp = _cpu_temp.group()[:-4]
    if _gpu_temp:
        gpu_temp = _gpu_temp.group().strip()[:-1]

    if int(cpu_temp) > threshold or int(gpu_temp) > threshold:
        return '{}|{}'.format(cpu_temp, gpu_temp)

def getUtilization(qtile:Optional[Qtile]=None, threshold:int=-1):
    try:
        cpu = subprocess.check_output(['top', '-bn2', '-d0.1']).decode()
    except:
        cpu = ""
    try:
        gpu = subprocess.check_output(
            ['nvidia-smi', '-q', '-d', 'UTILIZATION']).decode()
    except:
        gpu = ""

    if not cpu and not gpu:
        return 'error'

    _cpu_util = re.search(r'load average:\s(\d+\.\d+)', cpu) if cpu else None
    _gpu_util = re.search(r'Gpu\s+:\s\d+', gpu) if gpu else None
    cpu_util = gpu_util = 0
    if _cpu_util:
        u = _cpu_util.group().split(':')[-1].strip()
        cpu_util = '{:0.0f}'.format(float(u) * 100 / os.cpu_count())
    if _gpu_util:
        gpu_util = _gpu_util.group().split(':')[-1].strip()

    if int(cpu_util) > threshold or int(gpu_util) > threshold:
        return "{}|{}".format(cpu_util, gpu_util)

def powerClicked(qtile:Optional[Qtile]=None, button:int=1, power_button:int=1):
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

def updateWallpaper(qtile:Optional[Qtile]=None, adjustWindowCount=0, setSolid=False):
    if setSolid:
        wall = "Wallpaper"
    else:
        groups = qtile.cmd_groups()
        windows = adjustWindowCount
        for group in groups:
            if groups[group]["screen"] is None:
                continue
            windows += len(groups[group]["windows"])
        wall = "BlurredWallpaper" if windows > 0 else "Wallpaper"

    wallPath = os.path.expanduser("~/Pictures/") + wall
    cmd = "feh --bg-fill " + wallPath
    subprocess.Popen(cmd.split())
    #p = subprocess.Popen(cmd.split(), stderr=subprocess.PIPE, stdout=subprocess.PIPE)
    #stdout, stderr = p.communicate()
    # if stdout or stderr:
    #    logger.warning("out = {}, err = {}".format(stdout , stderr))
