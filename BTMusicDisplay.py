import kivy
kivy.require('1.10.0')

from kivy.uix.gridlayout import GridLayout
from kivy.properties import NumericProperty, ObjectProperty, StringProperty
from kivy.clock import Clock

import dbus
import gi

gi.require_version('Gst', '1.0')


'''
D-Bus stuff for accessing AVRCP through Bluez:
Name: org.bluez

Object path: /org/bluez/hci0/dev_B4_BF_F6_8C_FC_BF
Interface: org.bluez.MediaControl1
Methods:
- FastForward()
- Next()
- Pause()
- Play()
- Previous()
- Rewind()
- Stop()

Object path: /org/bluez/hci0/dev_B4_BF_F6_8C_FC_BF/player0
Interface: org.bluez.MediaPlayer1
Methods:
- FastForward()
- Next()
- Pause()
- Play()
- Previous()
- Rewind()
- Stop()
Properties:
- Repeat (boolean)
- Shuffle (boolean)
- Status (string; "paused" or similar)
- Track (dict of track info)
- Position (uint32)
'''


class BTMusicDisplay(GridLayout):
    position = NumericProperty()
    duration = NumericProperty()
    artist = StringProperty()
    album = StringProperty()
    track = StringProperty()

    def __init__(self, **kwargs):
        super(BTMusicDisplay, self).__init__(**kwargs)
        self.dbus = dbus.SystemBus()
        self.refreshBTDevice()

        Clock.schedule_interval(self.checkUpdate, 0.01)

    def refreshBTDevice(self):
        rootBTObj = self.dbus.get_object('org.bluez', '/')
        managedObjects = rootBTObj.GetManagedObjects(dbus_interface='org.freedesktop.DBus.ObjectManager')

        self.playerDevicePath = None
        self.playerDevice = None

        for path in managedObjects:
            if path.endswith('/player0'):
                print(f'Found media player: {path}')

                self.playerDevicePath = path
                self.playerDevice = dbus.Interface(
                    self.dbus.get_object('org.bluez', self.playerDevicePath),
                    dbus_interface='org.bluez.MediaPlayer1',
                )
                self.playerPropsDevice = dbus.Interface(
                    self.dbus.get_object('org.bluez', self.playerDevicePath),
                    dbus_interface='org.freedesktop.DBus.Properties',
                )

    def getPlayer(self):
        self.dbus.get_object('org.bluez', self.playerDevicePath)

    def previous(self):
        self.playerDevice.Previous()
        self.checkUpdate()

    def next(self):
        self.playerDevice.Next()
        self.checkUpdate()

    def play(self):
        self.playerDevice.Play()
        self.checkUpdate()

    def pause(self):
        self.playerDevice.Pause()
        self.checkUpdate()

    def getPlayerProp(self, name):
        return self.playerPropsDevice.Get('org.bluez.MediaPlayer1', name)

    def checkUpdate(self, *args):
        if self.playerDevicePath is None or self.playerDevice is None:
            self.position = 0
            self.duration = 1
            self.artist = '-'
            self.album = '-'
            self.track = '-'
            return

        self.position = int(self.getPlayerProp('Position'))

        track = self.getPlayerProp('Track')
        self.duration = int(track['Duration'])
        self.artist = track['Artist']
        self.album = track['Album']
        self.track = track['Title']
