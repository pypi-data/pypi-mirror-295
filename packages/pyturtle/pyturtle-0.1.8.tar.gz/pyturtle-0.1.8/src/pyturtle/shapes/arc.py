from typing import Dict, Optional, Tuple
from math import cos, sin, pi, radians

from turtle import Turtle
from pyturtle.shapes.shape import Shape
from pyturtle.shapes.point import Point2D


class Arc(Shape):
    def __init__(
        self,
        num_coordinates=100,
        center: Optional[Tuple[float, float]] = None,
        radius: float = 10,
        start_angle: float = 0,
        end_angle: float = 45,
    ):
        super().__init__(num_coordinates)
        self.center = Point2D(0, 0) if center is None else Point2D(*center)
        self.radius = radius
        self.start_angle = start_angle
        self.end_angle = end_angle

    def set_coordinates(self):
        """Generate coordinates for the arc based on the number of coordinates."""
        arc_length = self.end_angle - self.start_angle
        angle_increment = arc_length / (self.num_coordinates - 1)

        self.coordinates = [
            Point2D(
                round(
                    self.center.x
                    + self.radius
                    * cos(radians(self.start_angle + angle_increment * i)),
                    2,
                ),
                round(
                    self.center.y
                    + self.radius
                    * sin(radians(self.start_angle + angle_increment * i)),
                    2,
                ),
            )
            for i in range(self.num_coordinates)
        ]

    def get_slice():
        pass

    # def get_slice(self, step_num_one, step_num_two):
    #     """

    #     """
    #     slice_coordinates = {}
    #     t_in_arc_range = (t >= step_num_one and t <= step_num_two)
    #     for t in self._get_radians_lin_split():
    #         if t_in_arc_range:
    #             slice_coordinates[t] =
    #             for step, t in enumerate(self.coordinates.items())
    #         arc_coordinates[t] = {
    #             "x": self.coordinates[t]["x"],
    #             "y": self.coordinates[t]["y"],
    #         }
    # return arc_coordinates

    def get_random_slice(self):
        pass

    def translate_x(self, x_shift) -> None:
        """
        adds x_shift to x_coordinate of center to translate circle.
        a distance along x-axis x_shift length.
        """
        self.center.x = self.center.x + x_shift
        self.set_coordinates()

    def translate_y(self, y_shift) -> None:
        """
        adds y_shift to y_coordinate of center to translate circle
        a distance along y-axis y-shift length.
        """
        self.center.y = self.center.y + y_shift
        self.set_coordinates()

    def translate_xy(self, x_shift: float, y_shift: float) -> None:
        """
        shifts circle in both x and y direction.
        """
        self.center.x = self.center.x + x_shift
        self.center.y = self.center.y + y_shift
        self.set_coordinates()

    def rotate(self, angle: float) -> None:
        """
        rotates the circle
        """
        # positive angle rotates clockwise
        self.start_angle -= angle
        self.end_angle -= angle
        self.set_coordinates()

    def set_center(self, x, y):
        self.center = Point2D(x, y)

    def set_radius(self, r):
        self.radius = r
        self.set_coordinates()
