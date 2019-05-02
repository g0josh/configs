import subprocess
import time

from libqtile.widget import base

import iwlib
import psutil
from mpd import MPDClient, ConnectionError, CommandError


init_time = 0
init_speed = (0, 0)

class FuncOrTextWithClick(base.ThreadedPollText):
    """A generic text widget that polls using poll function to get the text"""
    orientations = base.ORIENTATION_HORIZONTAL
    defaults = [
        ('func', None, 'Poll Function'),
    ]

    def __init__(self, **config):
        base.ThreadedPollText.__init__(self, **config)
        self.add_defaults(FuncOrTextWithClick.defaults)
        if self.func:
            self._text = self.func()
        else:
            self._text = ""

    def button_press(self, x, y, button):
        if self.click_func:
            return self.click_func(x, y, button)

    def button_release(self, x, y, button):
        if self.release_func:
            return self.release_func(x, y, button)

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
