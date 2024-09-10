import json
import time

from ios_device.remote.remote_lockdown import RemoteLockdownClient
from ios_device.servers.Instrument import InstrumentServer


def energy(rpc, pid):
    rpc._start()
    channel = "com.apple.xcode.debug-gauge-data-providers.Energy"
    attr = {}
    print("start", rpc.call(channel, "startSamplingForPIDs:", {pid}).selector)
    for i in range(10):
        ret = rpc.call(channel, "sampleAttributes:forPIDs:", attr, {pid})
        print(ret.selector)
        time.sleep(1)
    rpc.stop()


if __name__ == '__main__':

    with RemoteLockdownClient(('fd4e:bc05:7f2d::1', 50615)) as rsd:
        # print(f'start {bundleid}')
        rpc = InstrumentServer(rsd).init()
        energy(rpc, 443)
        rpc.stop()

    # rpc = InstrumentServer().init()
    # energy(rpc, 261)
    # rpc.stop()
