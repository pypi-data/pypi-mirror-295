from turtle import Turtle
from math import pi
from pyturtle.shapes.arc import Arc


class Circle(Arc):
    def __init__(
        self,
        num_coordinates: int = 100,
        center=(0, 0),
        radius: float = 10,
        start_angle=0,
        end_angle=360,
    ):
        super().__init__(num_coordinates, center, radius, start_angle, end_angle)
