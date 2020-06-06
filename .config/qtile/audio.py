from subprocess import check_output, CalledProcessError, Popen
import re

from libqtile.log_utils import logger

GET_SINK_DETAILS_RE = re.compile('\d+\s+sink\(s\)\s+available.([\s\S]*)\d+\s+source\(s\)\s+available.')
SINK_DETAILS_RE = re.compile('(\*)\s+index:\s+(\d+)|volume:\s+front-left:\s+\d+\s+/\s+(\d+)%|muted:\s+(\w+)')


def _getSinks(fullDetails=True):
    sinks = []
    active = {}
    if fullDetails:
        cmd =  "pacmd list sinks"
        try:
            pacmd = check_output(
                cmd.split()).decode()
        except CalledProcessError as e:
            print("Error while getting current sinks: ", e)
            return []
        
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
                if not found[2]:
                    logger.warn(f'Audio/GetSinks: Empty index: {_sinks}')
                    return [], {}
                this_sink['volume'] = int(found[2])
            elif _index == 2:
                if not found[3]:
                    logger.warn(f'Audio/GetSinks: Empty index: {_sinks}')
                    return [], {}
                this_sink['muted'] = True if found[3] == 'yes' else 'False'
                sinks.append(dict(this_sink))
                if this_sink['active']:
                    active = dict(this_sink)
                this_sink = {}
    else:
        sinksCmd = "pactl list short sinks|awk '{print $1}'"
        try:
            sinks = check_output(sinksCmd, shell=True).decode().strip().split()
        except CalledProcessError as e:
            print("Error while getting current sinks: ", e)
            return [], {}

    return sinks, active

sinks, active_sink = _getSinks()

def update():
    global sinks
    sinks = _getSinks()

def isMuted():
    '''
    Check if the active sink is muted
    returns True/False
    '''
    global active_sink
    if not active_sink:
        logger.warn(f'Audio/isMuted: no active sink: {active_sink}')
        return None
    return active_sink['muted']

def getVolume():
    '''
    Gets the active sink volume
    returns int. -1 if error
    '''
    global active_sink
    if not active_sink:
        logger.warn(f'Audio/getVolume: no active sink: {active_sink}')
        return -1
    return active_sink['volume']

def toggleMute():
    '''
    Toggles active sink mute state
    returns True is succeeded, False if error
    '''
    global active_sink
    if not active_sink:
        logger.warn(f'Audio/toggleMuted: no active sink: {active_sink}')
        return False
    muteCmd = f'pactl set-sink-mute {active_sink["index"]} toggle'.split()
    Popen(muteCmd)
    return True

def setVolume(value):
    '''
    Sets active sink volume
    args
    value:string -  "+5" or "-5" for incremental control
                     "5" or "7" for absolute control
    returns True is succeeded, False if error
    '''
    global active_sink
    if not active_sink:
        logger.warn(f'Audio/toggleMuted: no active sink: {active_sink}')
        return False
    volCmd = f'pactl set-sink-volume {active_sink["index"]} {value}'.split()
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
            logger.warn("Audio/setActiveSink: Invalid sink({}), expected {}".format(
                sink, ['prev', 'next', range(len(sinks))]))
            return False
        else:
            toSink = sink - 1

    # get sink inputs
    try:
        inputs = check_output(
            "pactl list short sink-inputs|awk '{print $1}'", shell=True).decode().strip().split()
    except CalledProcessError as e:
        print("Error while getting sink inputs: ", e)
        return False
    Popen("pacmd set-default-sink {}".format(sinks[toSink]['index']).split())
    for inp in inputs:
        cmd = f'pactl move-sink-input {inp} {sinks[toSink]}'
        Popen(cmd.split())
    return True

