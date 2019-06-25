import subprocess
import time
import re
import os

from libqtile.log_utils import logger

from socket import error as socket_error
import psutil

MOUSE_BUTTONS={
    'LEFT_CLICK':1,'RIGHT_CLICK':2, 'SCROLL_UP':4, 'SCROLL_DOWN':5
}

POWER_BUTTONS={
    'SHUT':0, 'LOGOUT':1, 'LOCK_SCREEN':2
}

try:
    import iwlib
except ModuleNotFoundError:
    WLAN = False
    logger.warning("Please install iwlib")
else:
    WLAN = True
    init_time = 0
    init_speed = (0, 0)

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
        logger.warning('Uknown mouse click = ',button)

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

def getWlan(interface='wlo1', widgets = [], ontexts=[], offtexts=[], error_text=''):
    global init_time, init_speed
    enabled = True
    error = False

    try:
        status = iwlib.get_iwconfig(interface)
    except AttributeError as e:
        logger.warning (e)
        error = True
        essid = False
    else:
        essid = status['ESSID'].decode().strip()

    if not essid:
        enabled = False

    if enabled:
        speed = ( psutil.net_io_counters(pernic=True)[interface][0],
                    psutil.net_io_counters(pernic=True)[interface][1])
        _time = time.time()
        try:
            ul, dl = [(now - last) / (_time - init_time) / 1024.0
                    for now, last in zip(speed, init_speed)]
            init_speed = speed
            init_time = _time
        except Exception as e:
            logger.warning (e)
            return error_text

    if widgets:
        if not isinstance(ontexts, list):
            ontexts = [ontexts]*len(widgets)
        elif len(ontexts) < len(widgets):
            ontexts += [ontexts[-1]] * (len(widgets) - len(ontexts))

        if not isinstance(offtexts, list):
            offtexts = [offtexts]*len(widgets)
        elif len(offtexts) < len(widgets):
            offtexts += [offtexts[-1]] * (len(widgets) - len(offtexts))

        for index, widget in enumerate(widgets):
            widget.update( ontexts[index] if enabled or error else offtexts[index])

    if enabled:
        return "{}|{:3.0f} kB/s".format(essid, dl)
    elif error:
        return error_text
    else:
        return ""

def getlocksStatus():
    result = {'Caps':False, 'Num':False}
    """Return a list with the current state of the keys."""
    try:
        output = subprocess.check_output(['xset', 'q']).decode()
        output = re.findall(r"(Caps|Num)\s+Lock:\s*(\w*)", output)
    except subprocess.CalledProcessError as e:
        logger.warning(e.output.decode().strip())
        return result

    for x, y in output:
        result[x] = True if y == 'on' else False

    return result

def getTemps():
    try:
        cpu = subprocess.check_output(['sensors']).decode().strip()
        gpu = subprocess.check_output(['nvidia-smi']).decode().strip()
    except subprocess.CalledProcessError as e:
        logger.warning(e.output.decode().strip())
        return 'error'

    result = ""
    _cpu_temp = re.search(r'\d+\.\d+°C', cpu, flags=re.UNICODE)
    _gpu_temp = re.search(r'\s\d+C\s', gpu)
    if _cpu_temp:
        result = _cpu_temp.group()[:-4]
    if _gpu_temp:
        gpu_temp = _gpu_temp.group().strip()[:-1]
        result = result + '|' + gpu_temp if result else gpu_temp
    return result

def getUtilization():
    try:
        cpu = subprocess.check_output(['top','-bn2','-d0.1']).decode()
        gpu = subprocess.check_output(['nvidia-smi','-q','-d', 'UTILIZATION']).decode()
    except subprocess.CalledProcessError as e:
        logger.warning (e.output.decode().strip())
        return 'error'

    result = ""
    _cpu_util = re.search(r'load average:\s(\d+\.\d+)', cpu)
    _gpu_util = re.search(r'Gpu\s+:\s\d+',gpu)
    if _cpu_util:
        u = _cpu_util.group().split(':')[-1].strip()
        result = '{:0.0f}'.format((float(u)*100/os.cpu_count()))
    if _gpu_util:
        u = _gpu_util.group().split(':')[-1].strip()
        result = result + '|' + u if result else u

    return result

def getNumScreens():
    try:
        o = subprocess.check_output(['xrandr']).decode()
    except subprocess.CalledProcessError as e:
        logger.warning(e.output.decode().strip())
        return 1
    else:
        return len(re.findall(r'\w+ connected \w+', o))

# ---------------------------------------------
# POWER
# ---------------------------------------------

def showPowerClicked(x, y, button, widgets, ontexts, offtexts):
    if button not in [MOUSE_BUTTONS['LEFT_CLICK'], MOUSE_BUTTONS['RIGHT_CLICK']]:
        return
    if not isinstance(ontexts, list):
        ontexts = [ontexts]*len(widgets)
    elif len(ontexts) < len(widgets):
        ontexts += [ontexts[-1]] * (len(widgets) - len(ontexts))

    if not isinstance(offtexts, list):
        offtexts = [offtexts]*len(widgets)
    elif len(offtexts) < len(widgets):
        offtexts += [offtexts[-1]] * (len(widgets) - len(offtexts))

    for index, widget in enumerate(widgets):
        widget.update( ontexts[index] if widget.text==offtexts[index] else offtexts[index])

def powerClicked(x, y, button, widget_button):
    if button not in [MOUSE_BUTTONS['LEFT_CLICK'], MOUSE_BUTTONS['RIGHT_CLICK']]:
        return

    if widget_button == POWER_BUTTONS['SHUT']:
        cmd = ['shutdown', 'now']
    elif widget_button == POWER_BUTTONS['LOGOUT']:
        cmd = ['qtile-cmd', '-o', 'cmd', '-f', 'shutdown']
    elif widget_button == POWER_BUTTONS['LOCK_SCREEN']:
        cmd = [os.path.expanduser("~/.config/qtile/lockscreen.sh")]

    if cmd:
        try:
            subprocess.run(cmd)
        except subprocess.CalledProcessError as e:
            logger.warning(e.output.decode().strip())

