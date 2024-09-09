from typing import Dict, Optional, Tuple
from math import cos, sin, pi
import numpy.typing as npt
import numpy as np

from decimal import Decimal

from turtle import Turtle
from pyturtle.shapes.shape import Shape
from pyturtle.shapes.point import Point2D


class Arc(Shape):

    def __init__(
        self,
        num_coordinates=100,
        #center: Point2D = Point2D(0, 0),
        center: Optional[Tuple[float, float]] = None,
        radius: float = 10,
        theta_start: float = 0,
        theta_range: float = ((2*np.pi)/8)
    ):
        super().__init__(num_coordinates)
        self.center = Point2D(0, 0) if center is None else Point2D(*center)
        self.radius = radius
        self.theta_start = theta_start
        self.theta_range = theta_range

    def set_coordinates(self, rads: float=0) -> None:
        """
        Parameters
        -------------
        rads allow you to rotate the circle
        """
        self.coordinates = [Point2D(
                self.center.x + self.radius * Decimal(cos(2 * pi * i / self.num_coordinates + rads)),
                self.center.y + self.radius * Decimal(sin(2 * pi * i / self.num_coordinates + rads))
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

    def rotate(self, rads: float) -> None:
        """
        rotates the circle so that the t-value mappings change
        """
        self.set_coordinates(rads=rads)

    def set_center(self, x, y):
        self.center = Point2D(x, y)

    def set_radius(self, r):
        self.radius = r
        self.set_coordinates()






