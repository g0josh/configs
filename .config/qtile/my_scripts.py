import subprocess
import time

from libqtile import bar
from libqtile.widget import base
from libqtile.widget.groupbox import _GroupBase
from libqtile.command import Client

import iwlib
import psutil
from mpd import MPDClient, ConnectionError, CommandError


init_time = 0
init_speed = (0, 0)


class GroupBoxText(_GroupBase):
    """A widget that graphically displays the current group"""
    orientations = base.ORIENTATION_HORIZONTAL
    defaults = [("border", "000000", "group box border color")]

    def __init__(self, track_group, active_fg_color, active_bg_color,
            inactive_fg_color, inactive_bg_color,
            urgent_fg_color, urgent_bg_color,  text=None, **config):
        _GroupBase.__init__(self, **config)
        self.add_defaults(GroupBoxText.defaults)
        self.track_group = track_group
        self.text = text
        self.label=" "
        self.active_fg_color = active_fg_color
        self.active_bg_color = active_bg_color
        self.inactive_fg_color = inactive_fg_color
        self.inactive_bg_color = inactive_bg_color
        self.urgent_fg_color = urgent_fg_color
        self.urgent_bg_color = urgent_bg_color
        self.selected_group = None

    def button_press(self, x, y, button):
        if self.selected_group:
            self.bar.screen.setGroup(self.selected_group)

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
            if g.name == self.track_group and (g.windows or g.screen):
                return g
        return None

    def draw(self):
        self.selected_group = self.get_group()

        if self.selected_group is None:
            return

        self.label = self.text if self.text else self.selected_group.label
        if self.text:
            if self.selected_group == self.qtile.currentGroup:
                self.foreground = self.active_bg_color
                self.background = self.bar.background
            elif self.group_has_urgent(self.selected_group):
                self.foreground = self.urgent_bg_color
                self.background = self.bar.background
            else:
                self.foreground = self.inactive_bg_color
                self.background = self.bar.background
        else:
            if self.selected_group == self.qtile.currentGroup:
                self.foreground = self.active_fg_color
                self.background = self.active_bg_color
            elif self.group_has_urgent(self.selected_group):
                self.foreground = self.urgent_fg_color
                self.background = self.urgent_bg_color
            else:
                self.foreground = self.inactive_fg_color
                self.background = self.inactive_bg_color
        self.drawer.clear(self.background or self.bar.background)
        self.drawbox(0, self.label, self.background, self.foreground)
        self.drawer.draw(offsetx=self.offset, width=self.width)

class FuncWithClick(base.ThreadedPollText):
    """A generic text widget that polls using poll function to get the text"""
    orientations = base.ORIENTATION_HORIZONTAL
    defaults = [
        ('func', None, 'Poll Function'),
        ('click_func', None, 'click function'),
        ('release_func', None, 'click release function')
    ]

    def __init__(self, **config):
        base.ThreadedPollText.__init__(self, **config)
        self.add_defaults(FuncWithClick.defaults)
        if self.func:
            self._text = self.func()
        else:
            self._text = ""

    def button_press(self, x, y, button):
        if self.click_func:
            self.click_func(x, y, button)
            # self.poll()

    def button_release(self, x, y, button):
        if self.release_func:
            self.release_func(x, y, button)
            # self.poll()

    def poll(self):
        if self.func:
            # self.text = self.func()
            return self.func()

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
    return "{}|{:4.0f} kB/s".format(essid,dl)

def getMpd():
    pass

if __name__ == '__main__':
    print(getVolumeIcon())
    print(getWlan())
