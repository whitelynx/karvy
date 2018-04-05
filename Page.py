import kivy
kivy.require('1.10.0')

from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ListProperty, ObjectProperty, StringProperty
from kivy.clock import Clock
from kivy.graphics import *


class Page(BoxLayout):
    title = StringProperty()
    color = ListProperty([0.2, 0.2, 0.2, 1])
    text_color = ListProperty([1, 1, 1, 1])
    background_image = ObjectProperty()
