import kivy
kivy.require('1.10.0')

from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ObjectProperty, StringProperty
from kivy.clock import Clock


# D-Bus stuff for accessing AVRCP through Bluez:
# Name: org.bluez
# Object path: /org/bluez/hci0/dev_B4_BF_F6_8C_FC_BF/player0
# Interface: org.bluez.MediaPlayer1
# Methods:
# - FastForward()
# - Next()
# - Pause()
# - Play()
# - Previous()
# - Rewind()
# - Stop()
# Properties:
# - Repeat (boolean)
# - Shuffle (boolean)
# - Status (string; "paused" or similar)
# - Track (dict of track info)
# - Position (uint32)

class BTMusicDisplay(BoxLayout):
    artist = StringProperty()
    album = StringProperty()
    track = StringProperty()

    def __init__(self, **kwargs):
        super(BTMusicDisplay, self).__init__(**kwargs)
        Clock.schedule_interval(self.update, 0.1)
        self.update()

    def update(self, *args):
        self.artist = '<some artist here>'
        self.album = '<some album here>'
        self.track = '<some track here>'
