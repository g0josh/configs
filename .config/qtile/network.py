class NetSpeeds(object):
    def __init__(self, interface="wlp2s0"):
        self.init_time = 0
        self.init_bytes_tx_rx = [0,0]
        self.interface = interface

    def getSpeed(self):
        bytes_tx_rx = []
        for f in ['/sys/class/net/{}/statistics/tx_bytes'.format(self.interface),
            '/sys/class/net/{}/statistics/rx_bytes'.format(self.interface)]:
            with open(f, 'r') as fo:
                bytes_tx_rx.append(int(fo.read()))
        _time = time.time()
        speeds = [ (x - y) / (_time - self.init_time)
                    for x, y in zip(bytes_tx_rx, self.init_bytes_tx_rx)]
        self.init_bytes_tx_rx = bytes_tx_rx
        self.init_time = _time
        speeds = ["{:3.0f} kB/s".format(x/1e3) if x<1e6 else "{:2.1f} MB/s".format(x/1e6) for x in speeds]
        return {'upload':speeds[0], 'download':speeds[1]}

def getInterfaces():
    return [x for x in os.listdir('/sys/class/net') if any(y in x for y in ['wl','eth','enp'])]

# def getConnectedWlanSSID()