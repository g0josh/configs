import subprocess
import time
from datetime import datetime, timedelta
import re
import os
from contextlib import contextmanager

from libqtile.log_utils import logger

from socket import error as socket_error

MOUSE_BUTTONS={
    'LEFT_CLICK':1,'RIGHT_CLICK':2, 'SCROLL_UP':4, 'SCROLL_DOWN':5
}

POWER_BUTTONS={
    'SHUT_DOWN':0, 'LOG_OUT':1, 'LOCK_SCREEN':2
}

# ---------------------------------------------
# VOLUME
# ---------------------------------------------

def _getPulseSinks():
    try:
        output = subprocess.check_output(['pactl','list','short','sinks']).decode()
    except subprocess.CalledProcessError as e:
        logger.warning (e.output.decode().strip())
        return []
    else:
        return re.findall(r'^\d', output, flags=re.MULTILINE)

pulse_sinks = _getPulseSinks()

def volumePressed(x, y, button, icon_widget=None, value_widget=None):
    if button in [MOUSE_BUTTONS['LEFT_CLICK'], MOUSE_BUTTONS['RIGHT_CLICK']]:
        toggleMuteVolume()
    elif button == MOUSE_BUTTONS['SCROLL_UP']:
        changeVolume('+5%')
    elif button == MOUSE_BUTTONS['SCROLL_DOWN']:
        changeVolume('-5%')
    else:
        logger.warning('Uknown mouse click = {}'.format(button))

    if icon_widget:
        icon_widget.update( icon_widget.poll() )

    if value_widget:
        value_widget.update( value_widget.poll() )

def isVolumeMuted(reverse=False):
    try:
        cmd = "pacmd list-sinks|grep 'muted'|awk '{print $2}'"
        muted = subprocess.check_output(cmd, shell=True).strip().decode()
    except subprocess.CalledProcessError as e:
        logger.warning(e.output.decode().strip())
        return 'error'

    if reverse:
        return muted == 'no'
    else:
        return muted == 'yes'

def getVolumeIcon(muted_icon='', icons=['', '', ''], volume=None):
    # check if muted
    if isVolumeMuted():
        return muted_icon

    # Check volume level
    if volume is None:
        try:
            output = subprocess.check_output(['pactl','list', 'sinks']).decode()
            volume = re.search(r'Volume:\sfront-left:\s\d+\s/\s+\d+', output)
            volume = int(volume.group().split('/')[-1].strip())
        except subprocess.CalledProcessError as e:
            logger.warning(e.output.decode().strip())
            return 'error'

    margin = 100 / len(icons)
    index, _ = divmod(volume, margin)
    if index >= len(icons):
        index = len(icons) - 1
    return icons[int(index)]

def getVolume():
    if isVolumeMuted():
        return ""
    try:
        output = subprocess.check_output(['pactl','list','sinks']).decode()
        volume = re.search(r'Volume:\sfront-left:\s\d+\s/\s+\d+', output)
    except subprocess.CalledProcessError as e:
        logger.warning (e.output.decode().strip())
        return 'error'

    if volume:
        volume = volume.group().split('/')[-1].strip() + '%'
    else:
        return 'error'
    return volume

def toggleMuteVolume():
    global pulse_sinks
    if not pulse_sinks:
        return
    for sink in pulse_sinks:
        subprocess.call(['pactl', 'set-sink-mute', sink, 'toggle'])

def changeVolume(value='+5%'):
    global pulse_sinks
    if not pulse_sinks:
        return
    for sink in pulse_sinks:
        subprocess.call(['pactl', 'set-sink-volume', sink, value])

# ---------------------------------------------
# MPD
# ---------------------------------------------

def getMpd(not_connected_text='', max_title_len=15):
    try:
        output = subprocess.check_output(['mpc']).decode()
    except subprocess.CalledProcessError as e:
        logger.warning (e.output.decode().strip())
        return error_text
    else:
        output = output.split('\n')
    title = output[0].split('-')[-1].strip()
    title = title[:12] + '...' if len(title)>max_title_len else "{}{}".format(title," "*(max_title_len-len(title)))
    time = output[1].split()[-2]
    return "{} - {}".format(title, time)

def clickMpd(x, y, button):
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
        logger.warning (e.output.decode().strip())

# ---------------------------------------------
# Internet
# ---------------------------------------------

net_speed_objects = []

class NetSpeeds(object):
    def __init__(self, interface="wlp2s0"):
        self.init_time = 0
        self.init_bytes_tx_rx = [0,0]
        self.interface = interface

    def getSpeed(self):
        bytes_tx_rx = []
        for f in ['/sys/class/net/{}/statistics/tx_bytes'.format(self.interface),
            '/sys/class/net/{}/statistics/rx_bytes'.format(self.interface)]:
            with open(f, 'r') as fo:
                bytes_tx_rx.append(int(fo.read()))
        _time = time.time()
        speeds = [ (x - y) / (_time - self.init_time)
                    for x, y in zip(bytes_tx_rx, self.init_bytes_tx_rx)]
        self.init_bytes_tx_rx = bytes_tx_rx
        self.init_time = _time
        speeds = ["{:3.0f} kB/s".format(x/1e3) if x<1e6 else "{:2.1f} MB/s".format(x/1e6) for x in speeds]
        return {'upload':speeds[0], 'download':speeds[1]}

def getInterfaces():
    return [x for x in os.listdir('/sys/class/net') if any(y in x for y in ['wl','enp'])]

def getWlan(interface='wlo1', widgets = [], ontexts=[], offtexts=[], error_text=''):
    try:
        output = subprocess.check_output(['connmanctl', 'services']).decode()
    except subprocess.CalledProcessError as e:
        logger.warning (e.output.decode().strip())
        return error_text
    else:
        services = [x for x in output.split('\n') if x.startswith('*AO') and 'wifi' in x]
    
    if not services:
        return ""
    essid = services[0].split()[1]

    #get speeds
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

def getLan(interface='enp24s0', error_text=''):
    #check if enabled:
    up = []
    for _file in ['/sys/class/net/{}/operstate'.format(interface),
                   '/sys/class/net/{}/carrier'.format(interface)]:
        if not os.path.exists(_file):
            print('error')
            return error_text
        try:
            with open(_file, 'r') as f:
                up.append( f.read().strip().lower() )
        except:
            up.append("-1")
    if up != ['up', '1']:
        return ""

    #get speeds
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

def getTime(format='%b %d, %A, %I:%M %p', timezone=None):
    def _get_time():
        now = datetime.now().astimezone()
        return (now + timedelta(seconds=0.5)).strftime(format)

    if timezone is not None:
        with setTimeZone(timezone):
            return _get_time()
    else:
        return _get_time()

def getlocksStatus():
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

def getTemps(x=0,y=0,button=1, threshold=40):
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

def getUtilization(x=0,y=0,button=1,threshold=10):
    try:
        cpu = subprocess.check_output(['top','-bn2','-d0.1']).decode()
        gpu = subprocess.check_output(['nvidia-smi','-q','-d', 'UTILIZATION']).decode()
    except subprocess.CalledProcessError as e:
        logger.warning (e.output.decode().strip())
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


def powerClicked(x, y, button, power_button):
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

def setupMonitors():
    try:
        o = subprocess.check_output(['xrandr']).decode()
    except subprocess.CalledProcessError as e:
        logger.warning(e.output.decode().strip())
        return

    cmd = ["xrandr"]
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
        elif 'disconnected' in e:
            cmd += ['--output', name, '--off']

    try:
        subprocess.run(cmd)
    except subprocess.CalledProcessError as e:
        logger.warning(e.output.decode().strip())