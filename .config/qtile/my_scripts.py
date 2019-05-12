import subprocess
import time
import re

from libqtile import bar
from libqtile.widget import base
from libqtile.widget.groupbox import _GroupBase
from libqtile.command import Client

import iwlib
import psutil

from socket import error as socket_error
from mpd import MPDClient, ConnectionError, CommandError

init_time = 0
init_speed = (0, 0)
mpd_client = MPDClient()
mpd_password = None
cpu_cores = 0


def getCpuCores():
    global cpu_cores

    with open('/proc/cpuinfo', 'r') as f:
        _file = f.read()

    cores = re.search(r'cpu cores\s:\s\d', _file)
    if cores:
        cpu_cores = cores.group().split(':')[1].strip()
    else:
        cpu_cores = 4

getCpuCores()

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
            # if g.name == self.track_group and (g.windows or g.screen):
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

class FuncWithClick(base.ThreadedPollText):
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
        if self.func:
            self._text = self.func(**self.func_args)
        else:
            self._text = ""

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
        cmd = ["/home/job/.config/qtile/pulse_mute.sh", "toggle"]
    elif button == 4:
        cmd = ["/home/job/.config/qtile/pulse_vol.sh", "+5%"]
    elif button == 5:
        cmd = ["/home/job/.config/qtile/pulse_vol.sh", "-5%"]
    else:
        cmd = None

    if cmd is None:
        return

    subprocess.call(cmd)

def isVolumeMuted():
    try:
        cmd = "pacmd list-sinks|grep 'muted'|awk '{print $2}'"
        muted = subprocess.check_output(cmd, shell=True).strip().decode()
    except subprocess.CalledProcessError as e:
        return err.output.decode().strip()

    return muted == 'yes'

def getVolumeIcon(muted_icon='婢', icons=['奄', '奔', '墳']):
    # check if muted
    if isVolumeMuted():
        return muted_icon

    # Check volume level
    try:
        cmd = "pactl list sinks | grep 'Volume: front' | awk '{print $5}'"
        output = subprocess.check_output(cmd, shell=True).strip().decode()
        volume = int(output[:-1])
    except subprocess.CalledProcessError as e:
        return err.output.decode().strip()

    margin = 100 / len(icons)
    index, _ = divmod(volume, margin)
    if index >= len(icons):
        index = len(icons) - 1
    return icons[int(index)]

def getVolume():
    if isVolumeMuted():
        return ""
    try:
        cmd = "pactl list sinks | grep 'Volume: front' | awk '{print $5}'"
        output = subprocess.check_output(cmd, shell=True).strip().decode()
    except subprocess.CalledProcessError as e:
        output = err.output.decode().strip()
    return output

def muteVolume():
    pass

def changeVolume():
    pass

def getWlan(interface='wlo1'):
    global init_time, init_speed

    status = iwlib.get_iwconfig(interface)
    essid = bytes(status['ESSID']).decode().strip()

    speed = ( psutil.net_io_counters(pernic=True)[interface][0],
                psutil.net_io_counters(pernic=True)[interface][1])
    _time = time.time()
    try:
        ul, dl = [(now - last) / (_time - init_time) / 1024.0
                for now, last in zip(speed, init_speed)]
        init_speed = speed
        init_time = _time
    except Exception as e:
        return e
    return "{}|{:4.0f} kB/s".format(essid, dl)

def mpd_reconnect(host='localhost', port='6600'):
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
    global mpd_client

    mpd_connected = mpd_reconnect(host, port)

    if not mpd_connected:
        return not_connected_text
    else:
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
    mpd_connected = mpd_reconnect()

    if not mpd_connected:
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
        output = err.output.decode()
    if output.startswith("Keyboard"):
        indicators = re.findall(r"(Caps|Num)\s+Lock:\s*(\w*)", output)
    result = ""
    if ('Caps', 'on') in indicators:
        result = caps_text
    if ('Num', 'on') in indicators:
        result = result+' '+num_text if result else num_text
    return result

def getTemps():
    try:
        cpu = subprocess.check_output(['sensors']).decode().strip()
        gpu = subprocess.check_output(['nvidia-smi']).decode().strip()
    except subprocess.CalledProcessError as e:
        return err.output.decode().strip()

    result = ""
    _cpu_temp = re.search(r'\d+\.\d+°C', cpu, flags=re.UNICODE)
    _gpu_temp = re.search(r'\s\d+C\s', gpu)
    if _cpu_temp:
        result = _cpu_temp.group()[:-2]
    if _gpu_temp:
        gpu_temp = _gpu_temp.group().strip()[:-1]
        result = result + '|' + gpu_temp if result else gpu_temp

    return result

def getUtilization():
    pass






