from subprocess import check_output, CalledProcessError, Popen
import re
import argparse

from libqtile.log_utils import logger

GET_SINK_DETAILS_RE = re.compile('\d+\s+sink\(s\)\s+available.([\s\S]*)\d+\s+source\(s\)\s+available.')
SINK_DETAILS_RE = re.compile('(\*?)\s+index:\s+(\d+)|volume:\s+front-left:\s+\d+\s+/\s+(\d+)%|volume:\s+mono:\s+\d+\s+/\s+(\d+)%|muted:\s+(\w+)')

sinks = []
active_sink = []

def _getSinks(fullDetails=True):
    sinks = []
    active = {}
    if fullDetails:
        cmd =  "pacmd list sinks"
        try:
            pacmd = check_output(
                cmd.split()).decode()
        except CalledProcessError as e:
            logger.warn("Error while getting current sinks: {}".format(e))
            return [], {}
        
        _sink_details = GET_SINK_DETAILS_RE.search(pacmd).group()
        _sinks = SINK_DETAILS_RE.findall(_sink_details)
        this_sink = {}
        for index, found in enumerate(_sinks):
            _index = index if index < 3 else index - 3
            if _index == 0:
                if not found[1]:
                    logger.warn(f'Audio/GetSinks: Empty index: {_sinks}')
                    return [], {}
                this_sink = {
                    'index': found[1],
                    'active': True if found[0] == "*" else False,
                    'position': len(sinks)
                }
            elif _index == 1:
                if not found[2] and not found[3]:
                    logger.warn(f'Audio/GetSinks: Empty volume: {_sinks}')
                    return [], {}

                this_sink['volume'] = int(found[3]) if not found[2] else int(found[2])
            elif _index == 2:
                if not found[4]:
                    logger.warn(f'Audio/GetSinks: Empty mute flag: {_sinks}')
                    return [], {}

                this_sink['muted'] = True if found[4] == 'yes' else 'False'
                sinks.append(dict(this_sink))
                if this_sink['active']:
                    active = dict(this_sink)
                this_sink = {}
    else:
        sinksCmd = "pactl list short sinks|awk '{print $1}'"
        try:
            sinks = check_output(sinksCmd, shell=True).decode().strip().split()
        except CalledProcessError as e:
            logger.warn("Error while getting current sinks: {}".format(e))
            return [], {}

    # logger.warn(sinks)
    return sinks, active

def update():
    """
     Re-fetches current data from pulse audio
    """
    global sinks, active_sink
    sinks, active_sink = _getSinks()

def isMuted(refresh=True):
    '''
    Check if the active sink is muted

    Args
    refresh:boolean - Re-fetches current data from pulse audio
    returns True/False
    '''
    global active_sink, sinks
    if refresh or not active_sink:
        sinks, active_sink = _getSinks()
    if not active_sink:
        logger.warning(f'Audio/toggleMuted: no active sink: {active_sink}')
        return False

    return active_sink['muted']

def getVolume(refresh=True):
    '''
    Gets the active sink volume

    Args:
    refresh:boolean - Re-fetches current data from pulse audio
    returns int. -1 if error
    '''
    global active_sink, sinks
    if refresh or not active_sink:
        sinks, active_sink = _getSinks()
    if not active_sink:
        logger.warning(f'Audio/toggleMuted: no active sink: {active_sink}')
        return 0
    return active_sink['volume']

def setMute(mute=2, refresh=False):
    '''
    Sets active sink mute state

    Args:
    mute:int        - 0-unmute, 1-mute, 2-toggle
    refresh:boolean - Re-fetches current data from pulse audio

    returns True is succeeded, False if error
    '''
    global active_sink, sinks
    if refresh or not active_sink:
        sinks, active_sink = _getSinks()
    if not active_sink:
        logger.warning(f'Audio/toggleMuted: no active sink: {active_sink}')
        return False
    cmd = 'toggle' if mute == 2 else str(mute)
    muteCmd = f'pactl set-sink-mute {active_sink["index"]} {cmd}'.split()
    
    try:
        Popen(muteCmd)
    except CalledProcessError as err:
        logger.warning("SetMute error : {}".format(err))
        return False

    return True

def setVolume(value, refresh=False):
    '''
    Sets active sink volume

    Args
    value:string -  "+5" or "-5" for incremental control
                     "5" or "7" for absolute control
                     "+5%" or "5%" is also valid
    refresh:boolean - Re-fetches current data from pulse audio
    returns True is succeeded, False if error
    '''
    global active_sink, sinks
    if refresh or not active_sink:
        sinks, active_sink = _getSinks()
    if not active_sink:
        logger.warning(f'Audio/toggleMuted: no active sink: {active_sink}')
        return False
    volCmd = f'pactl set-sink-volume {active_sink["index"]} {value.strip()}'.split()
    Popen(volCmd)
    return True

def setActiveSink(sink):
    '''
    Sets the active sink
    args:
    sink:string - "1" or any sink index number sets the corresponding sink as active
                    "next" or "prev" sets the next or previous sink as the active one
    '''
    global sinks, active_sink
    sinks, active_sink = _getSinks()
    toSink = 0
    sink = sink.strip().lower()
    if sink == 'next':
        toSink = active_sink['position'] + 1 if active_sink['position'] < len(sinks)-1 else 0
    elif sink == 'prev':
        toSink = active_sink['position'] - 1 if active_sink['position'] > 0 else len(sinks) - 1
    else:
        if sink > len(sinks):
            logger.warning("Audio/setActiveSink: Invalid sink({}), expected {}".format(
                sink, ['prev', 'next', range(len(sinks))]))
            return False
        else:
            toSink = sink - 1

    Popen("pacmd set-default-sink {}".format(sinks[toSink]['index']).split())
    active_sink = sinks[toSink]

    # Most of the time you dont need this
    # get sink inputs
    # try:
    #     inputs = check_output("pactl list short sink-inputs|awk '{print $1}'", shell=True).decode().strip().split()
    # except CalledProcessError as e:
    #     logger.warning("Error while getting sink inputs: {}"format(e))
    #     return False

    # for inp in inputs:
    #     cmd = f'pactl move-sink-input {inp} {sinks[toSink]["index"]}'
    #     Popen(cmd.split())

    return True
