import kivy
kivy.require('1.10.0')

from kivy.uix.effectwidget import EffectWidget
from kivy.uix.image import Image
from kivy.properties import BoundedNumericProperty, NumericProperty, ObjectProperty, StringProperty


class Gauge(EffectWidget):
    unit = StringProperty()
    value = NumericProperty(0)
    min = NumericProperty(0)
    max = NumericProperty(100)
    major_step = BoundedNumericProperty(10, min=0, errorvalue=0)
    minor_step = BoundedNumericProperty(1, min=0, errorvalue=0)
    rotation = BoundedNumericProperty(0, min=-180, max=180, errorvalue=0)
    theta = BoundedNumericProperty(180, min=10, max=350, errorvalue=180)
    diameter = BoundedNumericProperty(0, min=0, errorvalue=0)
    line_inset = BoundedNumericProperty(0, min=0, errorvalue=0)
    line_width = BoundedNumericProperty(2, min=0, errorvalue=0)
    needle_width = BoundedNumericProperty(4, min=2, errorvalue=2)
    padding = BoundedNumericProperty(5, min=0, errorvalue=0)
    background_image = ObjectProperty()

    def __init__(self, **kwargs):
        super(Gauge, self).__init__(**kwargs)

        self.background_image = Image(source='gauge-background.png').texture
        self.background_image.wrap = 'repeat'
        self.background_image.uvsize = (1, 1)


if __name__ == '__main__':
    from os.path import join, dirname, abspath

    from kivy.app import App
    from kivy.clock import Clock
    from kivy.lang import Builder
    from kivy.uix.boxlayout import BoxLayout
    from kivy.uix.label import Label
    from kivy.uix.slider import Slider

    Builder.load_file(join(dirname(abspath(__file__)), 'Gauge.kv'))

    class GaugeApp(App):
        increasing = NumericProperty(1)
        begin = NumericProperty(50)
        step = NumericProperty(0.1)

        def build(self):
            box = BoxLayout(orientation='horizontal', padding=5)
            self.gauge = Gauge(value=50)
            self.slider = Slider(orientation='vertical')
            self.valueLabel = Label(text='50')

            stepper = Slider(min=0, max=25)
            stepper.bind(value=lambda instance, value: setattr(self, 'step', value))

            rotator = Slider(min=-180, max=180)
            rotator.bind(value=lambda instance, value: setattr(self.gauge, 'rotation', value))

            sizer = Slider(min=10, max=350)
            sizer.bind(value=lambda instance, value: setattr(self.gauge, 'theta', value))

            box.add_widget(self.gauge)
            box.add_widget(self.slider)
            box.add_widget(self.valueLabel)
            box.add_widget(stepper)
            box.add_widget(rotator)
            box.add_widget(sizer)

            Clock.schedule_interval(lambda *t: self.gauge_increment(), 0.03)
            return box

        def gauge_increment(self):
            begin = self.begin
            begin += self.step * self.increasing
            if begin > 0 and begin < 100:
                self.gauge.value = self.slider.value = begin
                self.valueLabel.text = str(begin)
            else:
                self.increasing *= -1
            self.begin = begin

    GaugeApp().run()
