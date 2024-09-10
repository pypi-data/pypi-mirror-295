"""
启动 app
"""
import os
import sys

from ios_device.remote.remote_lockdown import RemoteLockdownClient

sys.path.append(os.getcwd())

from ios_device.servers.Instrument import InstrumentServer


def _launch_app(rpc, bundleid):
    rpc._start()

    def on_channel_message(res):
        print(res.auxiliaries, res.selector)

    channel = "com.apple.instruments.server.services.processcontrol"
    rpc.register_channel_callback(channel, on_channel_message)
    pid = rpc.call(channel, "launchSuspendedProcessWithDevicePath:bundleIdentifier:environment:arguments:options:", "",
                   bundleid, {}, [], {"StartSuspendedKey": 0, "KillExisting": 1}).selector
    print("start", pid)


if __name__ == '__main__':
    with RemoteLockdownClient(('fd4e:bc05:7f2d::1', 50615)) as rsd:
        # print(f'start {bundleid}')
        rpc = InstrumentServer(rsd).init()
        _launch_app(rpc, 'com.apple.MobileSMS')
        rpc.stop()
