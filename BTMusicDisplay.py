import kivy
kivy.require('1.10.0')

from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ObjectProperty, StringProperty
from kivy.clock import Clock


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
