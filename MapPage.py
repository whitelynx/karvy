from datetime import datetime

import kivy
kivy.require('1.10.0')

from kivy.uix.gridlayout import GridLayout
from kivy.clock import Clock
from kivy.logger import Logger
from kivy.properties import ListProperty, ObjectProperty, StringProperty

#from kivy.garden.mapview import MapSource
#from kivy.garden.mapview.mapview.utils import clamp

import googlemaps
import polyline

#from LineMapLayer import LineMapLayer

mapsAPIKey = "AIzaSyAkoAktzhHGfMtdagOkRK2G3gPd-CR5MCc"


class MapPage(GridLayout):
    def __init__(self, **kwargs):
        super(MapPage, self).__init__(**kwargs)
        self._line_layer = None
        self.gmaps = googlemaps.Client(key=mapsAPIKey)

    @property
    def line_layer(self):
        if self._line_layer is None:
            #self._line_layer = LineMapLayer()
            self.ids.mapview.add_layer(self._line_layer, mode='scatter')

        return self._line_layer

    def get_directions(self, fromAddr, toAddr):
        Logger.info(f'Getting directions from {fromAddr!r} to {toAddr!r}...')
        try:
            routes = self.gmaps.directions(
                fromAddr,
                toAddr,
                mode='driving',
                departure_time=datetime.now()
            )

            route = routes[0]
            self.line_layer.coordinates = polyline.decode(route['overview_polyline']['points'])

            bounds = route['bounds']
            minBound = bounds['southwest']['lat'], bounds['southwest']['lng']
            maxBound = bounds['northeast']['lat'], bounds['northeast']['lng']
            self.fit(minBound, maxBound)

        except googlemaps.exceptions.HTTPError as err:
            Logger.warn(f'Error from Google Maps API: {err}')

    def fit(self, *points):
        minX, minY = float('inf'), float('inf')
        maxX, maxY = float('-inf'), float('-inf')
        for (x, y) in points:
            minX = min(minX, x)
            minY = min(minY, y)
            maxX = max(minX, x)
            maxY = max(minY, y)

        #self.ids.mapview.center_on((minX + maxX) / 2, (minY + maxY) / 2)

#        pctBuffer = 0.05;
#        xBuffer = (maxX - minX) * pctBuffer;
#        yBuffer = (maxY - minY) * pctBuffer;
#        zoom = min(
#            floor(-log(4)*log(dx) + screen_width/tile_size)
#        )
#
#        self.ids.mapview.zoom = clamp(
#            zoom,
#            self.ids.mapview.map_source.get_min_zoom(),
#            self.ids.mapview.map_source.get_max_zoom()
#        )
