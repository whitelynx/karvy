from datetime import datetime
import random
from math import *
from pprint import pprint

from kivy.graphics import Color, Line, SmoothLine
from kivy.graphics.context_instructions import Translate, Scale
from kivy.clock import Clock

from kivy.garden.mapview.mapview.utils import clamp
from kivy.garden.mapview.mapview import MapLayer, MIN_LONGITUDE, MIN_LATITUDE, MAX_LATITUDE, MAX_LONGITUDE

import googlemaps
import polyline


with open('google-maps-directions.apikey', 'r') as f:
    mapsAPIKey = f.read()


class LineMapLayer(MapLayer):
    def __init__(self, **kwargs):
        super(LineMapLayer, self).__init__(**kwargs)
        self._coordinates = []
        self.zoom = 0

        self.add_nav_coords()
        Clock.schedule_once(self.draw_line, 0)

    @property
    def coordinates(self):
        return self._coordinates

    @coordinates.setter
    def coordinates(self, coordinates):
        self._coordinates = coordinates

        #: Since lat is not a linear transform we must compute manually
        self.line_points = [(self.get_x(lon), self.get_y(lat)) for lat, lon in coordinates]
        #self.line_points = [mapview.get_window_xy_from(lat, lon, mapview.zoom) for lat, lon in coordinates]

    def reposition(self):
        mapview = self.parent

        #: Must redraw when the zoom changes
        #: as the scatter transform resets for the new tiles
        if (self.zoom != mapview.zoom):
            self.draw_line()

    def add_nav_coords(self):
        gmaps = googlemaps.Client(key=mapsAPIKey)
        now = datetime.now()
        routes = gmaps.directions(
            "100 broad st weymouth ma",
            "rice passions malden ma",
            mode="transit",
            departure_time=now
        )
        self.coordinates = polyline.decode(routes[0]['overview_polyline']['points'])

    def get_x(self, lon):
        '''Get the x position on the map using this map source's projection
        (0, 0) is located at the top left.
        '''
        return clamp(lon, MIN_LONGITUDE, MAX_LONGITUDE) / 180.

    def get_y(self, lat):
        '''Get the y position on the map using this map source's projection
        (0, 0) is located at the top left.
        '''
        lat = clamp(-lat, MIN_LATITUDE, MAX_LATITUDE)
        lat = lat * pi / 180.
        return ((1.0 - log(tan(lat) + 1.0 / cos(lat)) / pi))

    def draw_line(self, *args):
        mapview = self.parent
        self.zoom = mapview.zoom

        # When zooming we must undo the current scatter transform
        # or the animation distorts it
        scatter = mapview._scatter
        map_source = mapview.map_source
        sx, sy, ss = scatter.x, scatter.y, scatter.scale
        vx, vy, vs = mapview.viewport_pos[0], mapview.viewport_pos[1], mapview.scale

        # Account for map source tile size and mapview zoom
        ms = pow(2.0, mapview.zoom) * map_source.dp_tile_size

        with self.canvas:
            # Clear old line
            self.canvas.clear()

            # Undo the scatter animation transform
            Scale(1 / ss, 1 / ss, 1)
            Translate(-sx, -sy)

            # Apply the get window xy from transforms
            Scale(vs, vs, 1)
            Translate(-vx, -vy)

            # Apply the what we can factor out
            # of the mapsource long, lat to x, y conversion
            Scale(ms / 2.0, ms / 2.0, 1)
            Translate(1, 0)

            # Draw new
            Color(0, 0.2, 0.7, 0.25)
            Line(points=self.line_points, width=6.5 / ms)
            Color(0, 0.2, 0.7, 1)
            Line(points=self.line_points, width=6 / ms)
            Color(0, 0.3, 1, 1)
            Line(points=self.line_points, width=4 / ms)
            #Line(points=self.line_points, width=1)#4 / ms)#, joint='round', joint_precision=100)
            #Line(points=self.line_points, width=4 / ms, joint='round', close=False, cap='none')
            #Line(points=self.line_points, width=1)
