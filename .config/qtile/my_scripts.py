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

class GroupTextBox(_GroupBase):
    """A widget that graphically displays the current group"""
    orientations = base.ORIENTATION_HORIZONTAL
    defaults = [("border", "000000", "group box border color")]

    def __init__(self, track_group, **config):
        _GroupBase.__init__(self, **config)
        self.add_defaults(GroupTextBox.defaults)
        self.active_fg = config['active_fg']
        self.active_bg = config['active_bg']
        self.inactive_fg = config['inactive_fg']
        self.inactive_bg = config['inactive_bg']
        self.urgent_fg = config['urgent_fg']
        self.urgent_bg = config['urgent_bg']
        self.track_group = str(track_group)
        self.tracking_group = None
        self.label = str(config['label'])
        self.font = config['font']
        self.font_size = config['fontsize']

    def button_press(self, x, y, button):
        self.bar.screen.cmd_next_group()

    def calculate_length(self):
        # return self.box_width(self.qtile.groups)
        # l = self.text if self.text else self.tracking_group.label
        width, _ = self.drawer.max_layout_size(
           [self.label],
           self.font,
           self.fontsize
        )
        return width + self.padding_x * 2 + self.borderwidth * 2

    def group_has_urgent(self, group):
        return len([w for w in group.windows if w.urgent]) > 0

    def get_group(self):
        for g in self.qtile.groups:
            if g.name == self.track_group:
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

    def __init__(self, **config):
        base.ThreadedPollText.__init__(self, **config)
        self.add_defaults(FuncWithClick.defaults)
        if self.func:
            self.text = self.func()
        else:
            self.text = ""

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

def getWlan(interface='wlp2s0'):
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
