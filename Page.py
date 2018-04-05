import kivy
kivy.require('1.10.0')

from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ListProperty, ObjectProperty, StringProperty


class Page(BoxLayout):
    title = StringProperty()
    tab_color = ListProperty([0.2, 0.2, 0.2, 0.8])
    text_color = ListProperty([1, 1, 1, 1])
    background_color = ListProperty([0.1, 0.1, 0.1, 1])
    background_image = ObjectProperty()
