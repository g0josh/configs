import subprocess
import time
from datetime import datetime, timedelta
import re
import os
from contextlib import contextmanager

from libqtile.log_utils import logger

from socket import error as socket_error
import psutil

MOUSE_BUTTONS={
    'LEFT_CLICK':1,'RIGHT_CLICK':2, 'SCROLL_UP':4, 'SCROLL_DOWN':5
}

POWER_BUTTONS={
    'SHUT_DOWN':0, 'LOG_OUT':1, 'LOCK_SCREEN':2
}

try:
    import iwlib
except ModuleNotFoundError:
    logger.warning("Please install iwlib")

net_speed_objects = []

class NetSpeeds(object):
    def __init__(self, interface="wlp2s0"):
        self.init_time = 0
        self.init_bytes_tx_rx = (0,0)
        self.interface = interface

    def getSpeed(self):
        bytes_tx_rx = ( psutil.net_io_counters(pernic=True)[self.interface][0],
                    psutil.net_io_counters(pernic=True)[self.interface][1])
        _time = time.time()
        speeds = [ (x - y) / (_time - self.init_time)
                    for x, y in zip(bytes_tx_rx, self.init_bytes_tx_rx)]
        self.init_bytes_tx_rx = bytes_tx_rx
        self.init_time = _time
        speeds = ["{:3.0f} kB/s".format(x/1e3) if x<1e6 else "{:2.1f} MB/s".format(x/1e6) for x in speeds]
        return {'upload':speeds[0], 'download':speeds[1]}

try:
    from mpd import MPDClient, ConnectionError, CommandError
except ModuleNotFoundError:
    MPD = False
    logger.warning("Please install mpd")
else:
    mpd_client = MPDClient()
    mpd_password = None
    MPD = True

def _getPulseSinks():
    try:
        output = subprocess.check_output(['pactl','list','short','sinks']).decode()
    except subprocess.CalledProcessError as e:
        logger.warning (e.output.decode().strip())
        return []
    else:
        return re.findall(r'^\d', output, flags=re.MULTILINE)

pulse_sinks = _getPulseSinks()

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

# ---------------------------------------------
# VOLUME
# ---------------------------------------------

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

def mpd_reconnect(host='localhost', port='6600'):
    global MPD
    if not MPD:
        return False

    global mpd_client, mpd_password
    try:
        mpd_client.ping()
    except(socket_error, ConnectionError):
        try:
            mpd_client.connect(host, port)
            if mpd_password:
                mpd_client.password(mpd_password)
        except (socket_error, ConnectionError, CommandError):
            return False
    return True

def getMpd(not_connected_text='', host='localhost', port='6600'):
    if not mpd_reconnect(host, port):
        return not_connected_text

    global mpd_client
    mpd_client.command_list_ok_begin()
    mpd_client.status()
    mpd_client.currentsong()
    status, current_song = mpd_client.command_list_end()
    for e in ['artist', 'title']:
        if e in current_song:
            if len(current_song[e]) > 15:
                current_song[e] = current_song[e][:12] + '...'
            elif len(current_song[e]) < 15:
                current_song[e] = f"{current_song[e]}{' '*(15-len(current_song[e]))}"
        else:
            current_song[e] = 'Unknown'
    for e in ['elapsed', 'duration']:
        mm, ss = divmod(float(status[e]), 60)
        status[e] = '{:02.0f}:{:02.0f}'.format(mm, ss)
    return "{} - {}/{}".format(current_song['title'], status['elapsed'], status['duration'])

def clickMpd(x, y, button):
    if not mpd_reconnect():
        return

    global mpd_client
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
    if button == keys["toggle"]:
        status = mpd_client.status()
        play_status = status['state']

        if play_status == 'play':
            mpd_client.pause()
        else:
            mpd_client.play()
    elif button == keys["stop"]:
        mpd_client.stop()
    elif button == keys["previous"]:
        mpd_client.previous()
    elif button == keys["next"]:
        mpd_client.next()

# ---------------------------------------------
# MISC
# ---------------------------------------------

def getTime(format='%b %d, %A, %I:%M %p', timezone=None):
    def _get_time():
        now = datetime.now().astimezone()
        return (now + timedelta(seconds=0.5)).strftime(format)

    if timezone is not None:
        with setTimeZone(timezone):
            return _get_time()
    else:
        return _get_time()

def getWlan(interface='wlo1', widgets = [], ontexts=[], offtexts=[], error_text=''):
    try:
        status = iwlib.get_iwconfig(interface)
    except (AttributeError,NameError) as e:
        logger.warning (e)
        error = True
        essid = False
    else:
        error = False
        essid = status['ESSID'].decode().strip()

    if error:
        return error_text
    elif not essid:
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
        return "{}|{}".format(essid, speed)

def getLan(interface='enp2s0', error_text=''):
    #check if enabled:
    up = []
    for _file in ['/sys/class/net/{}/operstate'.format(interface),
                   '/sys/class/net/{}/carrier'.format(interface)]:
        if not os.path.exists(_file):
            return error_text
        with open(_file, 'r') as f:
            up.append( f.read().strip().lower() )
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

def getNumScreens():
    try:
        o = subprocess.check_output(['xrandr']).decode()
    except subprocess.CalledProcessError as e:
        logger.warning(e.output.decode().strip())
        return 1
    else:
        return len(re.findall(r'\w+ connected \w+', o))

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

