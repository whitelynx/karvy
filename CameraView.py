import kivy
kivy.require('1.10.0')

from kivy.uix.boxlayout import BoxLayout
from kivy.properties import BooleanProperty
from kivy.logger import Logger


class CameraView(BoxLayout):
    play = BooleanProperty(False)

    def on_play(self, instance, play):
        Logger.debug(f'on_play: {play}')
