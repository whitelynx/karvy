#!/usr/bin/env python
from datetime import datetime
from random import randint

import kivy
kivy.require('1.10.0')

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.widget import Widget
from kivy.properties import NumericProperty, ReferenceListProperty, ObjectProperty
from kivy.vector import Vector
from kivy.clock import Clock


class BTMusicDisplay(BoxLayout):
    artistDisplay = ObjectProperty(None)
    albumDisplay = ObjectProperty(None)
    trackDisplay = ObjectProperty(None)
    browser = ObjectProperty(None)
    now = ObjectProperty(datetime.now(), rebind=True)

    def update(self, *args):
        self.artistDisplay.text = '<some artist here>'
        self.albumDisplay.text = '<some album here>'
        self.trackDisplay.text = '<some track here>'
        self.now = datetime.now()

    def reload(self, touch):
        print('reload: touch.button:', touch.button)
        if touch.button == 'right':
            self.browser.url = 'https://maps.google.com'


class KarvyApp(App):
    def build(self):
        btMusicDisplay = BTMusicDisplay()
        btMusicDisplay.update()
        Clock.schedule_interval(btMusicDisplay.update, 1.0/60.0)
        return btMusicDisplay


if __name__ == '__main__':
    KarvyApp().run()
