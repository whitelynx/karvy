import kivy
kivy.require('1.10.0')

from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ObjectProperty


class CameraView(BoxLayout):
    camera = ObjectProperty()
