import kivy
kivy.require('1.10.0')

from kivy.animation import Animation
from kivy.uix.scrollview import ScrollView
from kivy.properties import AliasProperty, BooleanProperty, ListProperty, NumericProperty, ObjectProperty, OptionProperty, StringProperty
from kivy.clock import Clock
from kivy.logger import Logger

class ScrollingLabel(ScrollView):
    def get_texture_size(self):
        return self.label.texture_size

    text = StringProperty()
    label = ObjectProperty(None)
    texture_size = AliasProperty(get_texture_size, None, bind=('label',))
    duration = NumericProperty(10)
    delay = NumericProperty(1)
    font_name = StringProperty('fonts/Exo2-Regular.ttf')
    font_size = NumericProperty('15sp')
    line_height = NumericProperty(1.0)
    markdown = BooleanProperty(False)
    bold = BooleanProperty(False)
    italic = BooleanProperty(False)
    color = ListProperty([1, 1, 1, 1])
    valign = OptionProperty('bottom', options=['bottom', 'middle', 'top'])
    halign = OptionProperty('left', options=['left', 'center', 'right', 'justify'])

    l_size_hint_x = NumericProperty(1, allownone=True)
    l_size_hint_y = NumericProperty(1, allownone=True)

    def __init__(self, **kwargs):
        super(ScrollingLabel, self).__init__(**kwargs)

        #FIXME: This throws `TypeError: 'bool' object is not subscriptable`
        #self.anim = Animation(scroll_x=0, duration=self.delay) \
        #    + Animation(scroll_x=1, duration=self.duration) \
        #    + Animation(scroll_x=1, duration=self.delay) \
        #    + Animation(scroll_x=0, duration=self.duration)
        self.anim = Animation(scroll_x=1, duration=self.duration) \
            + Animation(scroll_x=0, duration=self.duration)

        self.anim.repeat = True
        self.anim.start(self)
