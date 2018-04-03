#!/usr/bin/env python
from datetime import datetime
from random import randint

import kivy
kivy.require('1.10.0')

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import DictProperty, ObjectProperty, StringProperty
from kivy.clock import Clock


class Screen(BoxLayout):
    now = ObjectProperty(datetime.now(), rebind=True)

    def __init__(self, **kwargs):
        super(Screen, self).__init__(**kwargs)
        Clock.schedule_interval(self.update, 0.1)
        self.update()

    def update(self, *args):
        self.now = datetime.now()



class Dashboard(BoxLayout):
    data = DictProperty({}, rebind=True)

    def update(self, **kwargs):
        self.data.update(kwargs)
        self.data = self.data


class WebDisplay(BoxLayout):
    browser = ObjectProperty(None)

    def reload(self, touch):
        print('reload: touch.button:', touch.button)
        if touch.button == 'right':
            self.browser.url = 'https://maps.google.com'


class KarvyApp(App):
    def build(self):
        return Screen()


if __name__ == '__main__':
    KarvyApp().run()
