from datetime import datetime

import kivy
kivy.require('1.10.0')

from kivy.uix.boxlayout import BoxLayout
from kivy.clock import Clock
from kivy.properties import ListProperty, ObjectProperty, StringProperty

from kivy.garden.mapview import MapSource

import googlemaps
import polyline

from LineMapLayer import LineMapLayer


with open('google-maps-directions.apikey', 'r') as f:
    mapsAPIKey = f.read()


class MapPage(BoxLayout):
    def __init__(self, **kwargs):
        super(MapPage, self).__init__(**kwargs)
        Clock.schedule_once(self.add_line_layer, 0)

    def add_line_layer(self, *args):
        gmaps = googlemaps.Client(key=mapsAPIKey)
        now = datetime.now()
        routes = gmaps.directions(
            '100 broad st weymouth ma',
            'rice passions malden ma',
            mode='driving',
            departure_time=now
        )

        line = LineMapLayer()
        line.coordinates = polyline.decode(routes[0]['overview_polyline']['points'])

        self.ids.mapview.add_layer(line, mode='scatter')
