import enum
import functools
from subprocess import check_output, CalledProcessError, Popen
import subprocess
import re

from libqtile.log_utils import logger

GET_SINK_DETAILS_RE = re.compile(
    '\d+\s+sink\(s\)\s+available.([\s\S]*)\d+\s+source\(s\)\s+available.')
SINK_DETAILS_RE = re.compile(
    '(\*?)\s+index:\s+(\d+)|volume:\s+front-left:\s+\d+\s+/\s+(\d+)%|volume:\s+mono:\s+\d+\s+/\s+(\d+)%|muted:\s+(\w+)')
GET_VOL_RE = re.compile('\[(\d+)\%\]')
GET_MUTED_RE = re.compile('\[\d+\%\]\s\[(\w+)\]')
GET_SINKS_RE = re.compile('\d+\t([^\s]+)')

def _getSinks():
    cmd = "pactl list short sinks"
    active_sink_cmd = 'pactl get-default-sink'
    try:
        raw_sinks = check_output(cmd.split()).decode().strip()
        active_sink = check_output(active_sink_cmd.split()).decode().strip()
    except CalledProcessError as e:
        logger.warn("Error while getting current sinks: {}".format(e))
        return [] 

    _sinks = GET_SINKS_RE.findall(raw_sinks)
    sinks = []
    for name in _sinks:
        sinks.append((name, active_sink == name))

    return sinks

def isMuted() -> bool:
    '''
    Check if the active sink is muted

    Args
    refresh:boolean - Re-fetches current data from pulse audio
    returns True/False
    '''
    try:
        rawVol = check_output('amixer get Master'.split()).decode()
        muted = GET_MUTED_RE.search(rawVol).groups()[0]
        return muted == 'off'
    except CalledProcessError as err:
        logger.warning("audio getMuted error : {}".format(err))
        return False


def getVolume() -> str:
    '''
    Gets the active sink volume

    Args:
    returns int 
    '''
    try:
        rawVol = check_output('amixer get Master'.split()).decode()
        return int(GET_VOL_RE.search(rawVol).groups()[0])
    except CalledProcessError as err:
        logger.warning("audio getVolume error : {}".format(err))
        return ''


def setMute(action='toggle') -> bool:
    '''
    Sets active sink mute state

    Args:
    action:str        - mute, unmute, toggle
    returns True if carried out successfully else False
    '''
    muteCmd = f'amixer -q sset Master {action}'.split()

    try:
        subprocess.run(muteCmd)
    except CalledProcessError as err:
        logger.warning("SetMute error : {}".format(err))
        return False

    return True


def setVolume(value) -> bool:
    '''
    Sets active sink volume

    Args
    value:string -  "5%+" or "5%-" for incremental control
                     "5%" or "7%" for absolute control
    returns True if carried out successfully else False
    '''
    volCmd = f'amixer -q set Master {value.strip()}'.split()
    try:
        subprocess.run(volCmd)
    except CalledProcessError as err:
        logger.warning("SetVolume error : {}".format(err))
        return False

    return True

def setActiveSink(sink_name: str):
    '''
    Sets the active sink
    args:
    sink:string - any sink name ( from pactl list sinks command)
                  "next" or "prev" sets the next or previous sink as the active one
    '''
    to_sink = None
    if sink_name not in ['prev', 'next']:
        to_sink = sink_name
    else:
        sinks = _getSinks()
        if not sinks:
            logger.warn('No sinks found to set active sink')
            return

        active_sink_index = None
        for index, (_, active) in enumerate(sinks):
            if active:
                active_sink_index = index
                break
        if active_sink_index is None:
            logger.warn("No active index found while setting active sink")
            return
        
        if sink_name == 'next':
            to_sink = sinks[active_sink_index + 1 if active_sink_index+1 < len(sinks) else 0][0]
        elif sink_name == 'prev':
            to_sink = sinks[active_sink_index - 1 if active_sink_index > 0 else len(sinks)-1][0]

    if to_sink:
        Popen("pactl set-default-sink {}".format(to_sink).split())
    else:
        logger.warn('No sink to set active sink')