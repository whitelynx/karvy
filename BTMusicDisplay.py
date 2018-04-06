from datetime import timedelta

import kivy
kivy.require('1.10.0')

from kivy.uix.gridlayout import GridLayout
from kivy.properties import AliasProperty, BooleanProperty, NumericProperty, ObjectProperty, StringProperty
from kivy.clock import Clock
from kivy.logger import Logger

import dbus

from DBus import systemBus


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


def renderMS(ms):
    return str(timedelta(milliseconds=ms))


class BTMusicDisplay(GridLayout):
    player_name = StringProperty()
    status = StringProperty()
    shuffle = BooleanProperty()
    repeat = BooleanProperty()
    position = NumericProperty()
    duration = NumericProperty()
    artist = StringProperty()
    album = StringProperty()
    track = StringProperty()

    def get_status_display(self):
        if self.duration:
            return f'{self.status} [size=11][font=fonts/OxygenMono-Regular.ttf]({renderMS(self.position)[:-5]} / {renderMS(self.duration)})[/font][/size]'
        return self.status

    status_display = AliasProperty(get_status_display, None, bind=('status', 'position', 'duration'))

    def __init__(self, **kwargs):
        super(BTMusicDisplay, self).__init__(**kwargs)
        self.refreshBTDevice()

        self.triggerRefreshBTDevice = Clock.create_trigger(self.refreshBTDevice)
        self.triggerUpdate = Clock.create_trigger(self.checkUpdate)

        Clock.schedule_interval(self.triggerUpdate, 0.01)

    def refreshBTDevice(self, *args):
        rootBTObj = systemBus.get_object('org.bluez', '/')
        managedObjects = rootBTObj.GetManagedObjects(dbus_interface='org.freedesktop.DBus.ObjectManager')

        self.playerObjectPath = None
        self.player = None

        for path in managedObjects:
            if path.endswith('/player0'):
                Logger.info(f'BTMusicDisplay: Found media player: {path}')

                self.playerObjectPath = path

                deviceObject = systemBus.get_object('org.bluez', self.playerObjectPath[:-8])
                self.player_name = deviceObject.Get(
                    'org.bluez.Device1',
                    'Alias',
                    dbus_interface='org.freedesktop.DBus.Properties'
                )

                self.player = dbus.Interface(
                    systemBus.get_object('org.bluez', self.playerObjectPath),
                    dbus_interface='org.bluez.MediaPlayer1',
                )
                self.playerPropsDevice = dbus.Interface(
                    systemBus.get_object('org.bluez', self.playerObjectPath),
                    dbus_interface='org.freedesktop.DBus.Properties',
                )

                self.checkUpdate()

    def getPlayer(self):
        systemBus.get_object('org.bluez', self.playerObjectPath)

    def previous(self):
        self.player.Previous()

    def next(self):
        self.player.Next()

    def play(self):
        self.player.Play()

    def pause(self):
        self.player.Pause()

    def getPlayerProp(self, name):
        return self.playerPropsDevice.Get('org.bluez.MediaPlayer1', name)

    def setPlayerProp(self, name, value):
        self.playerPropsDevice.Set('org.bluez.MediaPlayer1', name, value)

    def setDefaultValues(self):
        self.status = 'disconnected'
        self.position = 0
        self.duration = 0
        self.artist = '-'
        self.album = '-'
        self.track = '-'

    def checkUpdate(self, *args):
        if self.playerObjectPath is None or self.player is None:
            self.setDefaultValues()
            self.triggerRefreshBTDevice()
            return

        try:
            self.status = self.getPlayerProp('Status')
            self.position = int(self.getPlayerProp('Position'))
            self.shuffle = self.getPlayerProp('Shuffle')
            self.repeat = self.getPlayerProp('Repeat')

            track = self.getPlayerProp('Track')
            self.duration = int(track['Duration'])
            self.artist = track['Artist']
            self.album = track['Album']
            self.track = track['Title']

        except dbus.exceptions.DBusException:
            self.setDefaultValues()
            self.triggerRefreshBTDevice()
