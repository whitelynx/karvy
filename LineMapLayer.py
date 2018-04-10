from math import *

from kivy.graphics import Color, Line, SmoothLine, MatrixInstruction
from kivy.graphics.context_instructions import Translate, Scale
from kivy.clock import Clock

from kivy.garden.mapview.mapview.utils import clamp
from kivy.garden.mapview.mapview import MapLayer, MIN_LONGITUDE, MIN_LATITUDE, MAX_LATITUDE, MAX_LONGITUDE


class LineMapLayer(MapLayer):
    def __init__(self, **kwargs):
        super(LineMapLayer, self).__init__(**kwargs)
        self._coordinates = []
        self._line_points = None
        self._line_points_offset = (0, 0)
        self._ms = None
        self.zoom = 0

    @property
    def coordinates(self):
        return self._coordinates

    @coordinates.setter
    def coordinates(self, coordinates):
        self._coordinates = coordinates
        self.invalidate_line_points()
        self.clear_and_redraw()

    @property
    def line_points(self):
        if self._line_points is None:
            self.calc_line_points()
        return self._line_points

    @property
    def line_points_offset(self):
        if self._line_points is None:
            self.calc_line_points()
        return self._line_points_offset

    @property
    def ms(self):
        if self._ms is None:
            mapview = self.parent
            map_source = mapview.map_source
            self._ms = pow(2.0, mapview.zoom) * map_source.dp_tile_size
        return self._ms

    def calc_line_points(self):
        # Offset all points by the coordinates of the first point, to keep coordinates closer to zero.
        # (and therefore avoid some float precision issues when drawing lines)
        self._line_points_offset = (self.get_x(self.coordinates[0][1]), self.get_y(self.coordinates[0][0]))
        # Since lat is not a linear transform we must compute manually
        self._line_points = [(self.get_x(lon) - self._line_points_offset[0], self.get_y(lat) - self._line_points_offset[1]) for lat, lon in self.coordinates]

    def invalidate_line_points(self):
        self._line_points = None
        self._line_points_offset = (0, 0)

    def get_x(self, lon):
        '''Get the x position on the map using this map source's projection
        (0, 0) is located at the top left.
        '''
        return clamp(lon, MIN_LONGITUDE, MAX_LONGITUDE) * self.ms / 360.0

    def get_y(self, lat):
        '''Get the y position on the map using this map source's projection
        (0, 0) is located at the top left.
        '''
        lat = radians(clamp(-lat, MIN_LATITUDE, MAX_LATITUDE))
        return ((1.0 - log(tan(lat) + 1.0 / cos(lat)) / pi)) * self.ms / 2.0

    def reposition(self):
        mapview = self.parent

        # Must redraw when the zoom changes
        # as the scatter transform resets for the new tiles
        if (self.zoom != mapview.zoom):
            self._ms = None
            self.invalidate_line_points()
            self.clear_and_redraw()

    def clear_and_redraw(self, *args):
        with self.canvas:
            # Clear old line
            self.canvas.clear()

        # FIXME: Why is 0.05 a good value here? Why does 0 leave us with weird offsets?
        Clock.schedule_once(self._draw_line, 0.05)

    def _draw_line(self, *args):
        mapview = self.parent
        self.zoom = mapview.zoom

        # When zooming we must undo the current scatter transform
        # or the animation distorts it
        scatter = mapview._scatter
        sx, sy, ss = scatter.x, scatter.y, scatter.scale

        # Account for map source tile size and mapview zoom
        vx, vy, vs = mapview.viewport_pos[0], mapview.viewport_pos[1], mapview.scale

        with self.canvas:
            # Clear old line
            self.canvas.clear()

            # Offset by the MapView's position in the window
            Translate(*mapview.pos)

            # Undo the scatter animation transform
            Scale(1 / ss, 1 / ss, 1)
            Translate(-sx, -sy)

            # Apply the get window xy from transforms
            Scale(vs, vs, 1)
            Translate(-vx, -vy)

            # Apply the what we can factor out of the mapsource long, lat to x, y conversion
            Translate(self.ms / 2, 0)

            # Translate by the offset of the line points (this keeps the points closer to the origin)
            Translate(*self.line_points_offset)

            # Draw line
            Color(0, 0.2, 0.7, 0.25)
            Line(points=self.line_points, width=6.5 / 2)
            Color(0, 0.2, 0.7, 1)
            Line(points=self.line_points, width=6 / 2)
            Color(0, 0.3, 1, 1)
            Line(points=self.line_points, width=4 / 2)
