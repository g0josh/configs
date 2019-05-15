import subprocess
import time
import re

from libqtile.log_utils import logger
from libqtile import bar
from libqtile.widget import base, TextBox
from libqtile.widget.groupbox import _GroupBase
from libqtile.command import Client, lazy

from socket import error as socket_error
import psutil

try:
    import iwlib
except ModuleNotFoundError:
    WLAN = False
    print("Please install iwlib")
else:
    WLAN = True
    init_time = 0
    init_speed = (0, 0)

try:
    from mpd import MPDClient, ConnectionError, CommandError
except ModuleNotFoundError:
    MPD = False
    print("Please install mpd")
else:
    mpd_client = MPDClient()
    mpd_password = None
    MPD = True

def _getCpuCores():
    with open('/proc/cpuinfo', 'r') as f:
        _file = f.read()

    cores = re.search(r'cpu cores\s:\s\d', _file)
    if cores:
        cpu_cores = int(cores.group().split(':')[1].strip())
    else:
        cpu_cores = 4

    return cpu_cores

def _getPulseSinks():
    try:
        output = subprocess.check_output(['pactl','list','short','sinks']).decode()
    except subprocess.CalledProcessError as e:
        print (err.output.decode().strip())
        return []
    else:
        return re.findall(r'^\d', output, flags=re.MULTILINE)

cpu_cores = _getCpuCores()
pulse_sinks = _getPulseSinks()


class CTextBox(base._TextBox):
    """A flexible textbox that can be updated from bound keys, scripts, and qshell"""
    orientations = base.ORIENTATION_HORIZONTAL
    defaults = [
        ("font", "sans", "Text font"),
        ("fontsize", None, "Font pixel size. Calculated if None."),
        ("fontshadow", None, "font shadow color, default is None(no shadow)"),
        ("padding", None, "Padding left and right. Calculated if None."),
        ("foreground", "#ffffff", "Foreground colour."),
    ]

    def __init__(self, text=" ", width=bar.CALCULATED, **config):
        base._TextBox.__init__(self, text=text, width=width, **config)

    def _configure(self, qtile, bar):
        _TextBox._configure(self, qtile, bar)

    def update(self, text):
        self.text = text
        self.bar.draw()

    def cmd_update(self, text):
        """Update the text in a TextBox widget"""
        self.update(text)

    def cmd_get(self):
        """Retrieve the text in a TextBox widget"""
        return self.text

id_ = 'S'
def mute(func):
    global id_
    # toggleMuteVolume()
    if id_ == 'S':
        func.update('N')
        id_ = 'N'
    else:
        # func('S')
        func.update('S')
        id_ = 'S'

class GroupTextBox(_GroupBase):
    """A widget that graphically displays the current group"""
    orientations = base.ORIENTATION_HORIZONTAL
    defaults = [("border", "000000", "group box border color")]

    def __init__(self, track_group, label, active_fg, active_bg,
            inactive_fg, inactive_bg, urgent_fg, urgent_bg,
            not_empty_fg, not_empty_bg, **config):
        _GroupBase.__init__(self, **config)
        self.add_defaults(GroupTextBox.defaults)
        self.track_group_name = track_group
        self.tracking_group = None
        self.label=label
        self.active_fg = active_fg
        self.active_bg = active_bg
        self.inactive_fg = inactive_fg
        self.inactive_bg = inactive_bg
        self.urgent_fg = urgent_fg
        self.urgent_bg = urgent_bg
        self.not_empty_fg = not_empty_fg
        self.not_empty_bg = not_empty_bg

    def button_press(self, x, y, button):
        if self.tracking_group:
            self.bar.screen.setGroup(self.tracking_group)

    def calculate_length(self):
        width, _ = self.drawer.max_layout_size(
           [self.label],
           self.font,
           self.fontsize
        )
        return width

    def group_has_urgent(self, group):
        return len([w for w in group.windows if w.urgent]) > 0

    def get_group(self):
        for g in self.qtile.groups:
            if g.name == self.track_group_name:
            #if g.name == self.track_group and (g.windows or g.screen):
                return g
        return None

    def draw(self):
        tracking_group = self.get_group()
        # if tracking_group is None:
        #     self.drawer.clear(self.bar.background)
        #     # self.drawbox(self.margin_x, " ", self.border, self.foreground)
        #     self.drawer.draw(offsetx=self.offset, width=self.width)
        #     # self.bar.draw()

        # if tracking_group == self.tracking_group:
            # return True
        self.tracking_group = tracking_group
        # self.text = self.tracking_group.label if self.text == 'NA' else self.text
        if self.tracking_group == self.qtile.currentGroup:
            self.foreground = self.active_fg
            self.background = self.active_bg
        elif self.group_has_urgent(self.tracking_group):
            self.foreground = self.urgent_fg
            self.background = self.urgent_bg
        elif self.tracking_group.windows or self.tracking_group.screen:
            self.foreground = self.not_empty_fg
            self.background = self.not_empty_bg
        else:
            self.foreground = self.inactive_fg
            self.background = self.inactive_bg

        self.drawer.clear(self.background or self.bar.background)
        self.drawbox(0, self.label, self.border, self.foreground)
        self.drawer.draw(offsetx=self.offset, width=self.width)

class FuncWithClick(base.ThreadPoolText):
    """A generic text widget that polls using poll function to get the text"""
    orientations = base.ORIENTATION_HORIZONTAL
    defaults = [
        ('func', None, 'Poll Function'),
        ('click_func', None, 'click function'),
        ('release_func', None, 'click release function')
    ]

    def __init__(self, func_args={}, click_func_args={}, **config):
        base.ThreadedPollText.__init__(self, **config)
        self.add_defaults(FuncWithClick.defaults)
        self.func_args = func_args
        self.click_func_args = click_func_args
        # if self.func:
        #     self._text = self.func(**self.func_args)
        # else:
        #     self._text = ""

    def button_press(self, x, y, button):
        if self.click_func:
            self.click_func(x, y, button, **self.click_func_args)
            self.poll()

    def button_release(self, x, y, button):
        if self.release_func:
            self.release_func(x, y, button, **self.click_func_args)
            self.poll()

    def poll(self):
        if self.func:
            # self.text = self.func()
            return self.func(**self.func_args)

def clickVolume(x, y, button):
    if button in [1,2]:
        toggleMuteVolume()
    elif button == 4:
        changeVolume("+5%")
    elif button == 5:
        changeVolume("-5%")

def isVolumeMuted():
    try:
        cmd = "pacmd list-sinks|grep 'muted'|awk '{print $2}'"
        muted = subprocess.check_output(cmd, shell=True).strip().decode()
    except subprocess.CalledProcessError as e:
        print (err.output.decode().strip())
        return 'error'

    return muted == 'yes'

def getVolumeIcon(muted_icon='婢', icons=['奄', '奔', '墳']):
    # check if muted
    if isVolumeMuted():
        return muted_icon

    # Check volume level
    try:
        output = subprocess.check_output(['pactl','list', 'sinks']).decode()
        volume = re.search(r'Volume:\sfront-left:\s\d+\s/\s+\d+', output)
    except subprocess.CalledProcessError as e:
        print (err.output.decode().strip())
        return 'error'

    if volume:
        volume = int(volume.group().split('/')[-1].strip())
    else:
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
        print (err.output.decode().strip())
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

def getWlan(interface='wlo1'):
    global init_time, init_speed
    status = iwlib.get_iwconfig(interface)
    essid = status['ESSID'].decode().strip()

    if not essid:
        return ""

    speed = ( psutil.net_io_counters(pernic=True)[interface][0],
                psutil.net_io_counters(pernic=True)[interface][1])
    _time = time.time()
    try:
        ul, dl = [(now - last) / (_time - init_time) / 1024.0
                for now, last in zip(speed, init_speed)]
        init_speed = speed
        init_time = _time
    except Exception as e:
        print (e)
        return 'error'

    return "{}|{:4.0f} kB/s".format(essid, dl)

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
                current_song[e] = current_song[e][:15] + '...'
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

def getCapsNumLocks(num_text='NUM', caps_text='CAPS'):
    """Return a list with the current state of the keys."""
    try:
        output = subprocess.check_output(['xset', 'q']).decode()
    except subprocess.CalledProcessError as err:
        print(err.output.decode().strip())
        return 'error'

    # if output.startswith("Keyboard"):
    indicators = re.findall(r"(Caps|Num)\s+Lock:\s*(\w*)", output)
    logger.warning(str(indicators))
    result = ""
    if ('Caps', 'on') in indicators:
        result = caps_text
    if ('Num', 'on') in indicators:
        result = result+' '+num_text if result else num_text
    return result

def locksPressed(widgets, ontexts, offtexts, numlock=False):
    if not widgets:
        print ("No widgets passed in for Caps lock pressed")
        return
    if not isinstance(widgets, list):
        print ("Widgets expected to be a list")
        return

    result = getCapsNumLocks(num_text='1', caps_text='A')
    to_check = '1' if numlock else 'A'
    locked = True if to_check in result else False

    if not isinstance(ontexts, list):
        ontexts = [ontexts]*len(widgets)
    elif len(ontexts) < len(widgets):
        ontexts += [ontexts[-1]] * (len(widgets)-len(ontexts))

    if not isinstance(offtexts, list):
        offtexts = [offtexts]*len(widgets)
    elif len(offtexts) < len(widgets):
        offtexts += [offtexts[-1]] * (len(widgets)-len(offtexts))

    logger.warning("({}) ,{},{}".format(result, to_check, locked))

    for index, widget in enumerate(widgets):
        if not isinstance(widget, TextBox):
            print ("{} is not a TextBox".format(widget))
            continue
        if locked:
            widget.update(ontexts[index])
        else:
            widget.update(offtexts[index])

def getTemps():
    try:
        cpu = subprocess.check_output(['sensors']).decode().strip()
        gpu = subprocess.check_output(['nvidia-smi']).decode().strip()
    except subprocess.CalledProcessError as e:
        print (err.output.decode().strip())
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
        print (err.output.decode().strip())
        return 'error'

    result = ""
    _cpu_util = re.search(r'load average:\s(\d+\.\d+),\s(\d+\.\d+)', cpu)
    _gpu_util = re.search(r'Gpu\s+:\s\d+',gpu)
    if _cpu_util:
        global cpu_cores
        u = _cpu_util.group().split(',')[-1].strip()
        result = '{:0.0f}'.format((float(u)*100/cpu_cores))
    if _gpu_util:
        u = _gpu_util.group().split(':')[-1].strip()
        result = result + '|' + u if result else u

    return result