import kivy
kivy.require('1.10.0')

from kivy.uix.boxlayout import BoxLayout
from kivy.clock import Clock
from kivy.properties import ListProperty, ObjectProperty, StringProperty

from kivy.garden.mapview import MapSource

from LineMapLayer import LineMapLayer


class MapPage(BoxLayout):
    def __init__(self, **kwargs):
        super(MapPage, self).__init__(**kwargs)
        Clock.schedule_once(self.add_line_layer, 0)

    def add_line_layer(self, *args):
        line = LineMapLayer()
        self.ids.mapview.add_layer(line, mode='scatter')
