from turtle import Turtle
from math import pi
from pyturtle.shapes.arc import Arc

class Circle(Arc):
    def __init__(self, num_coordinates: int=100, center = (0, 0), radius: float=10, theta_start: float=0, theta_range:float=2*pi):
        super().__init__(num_coordinates, center, radius, theta_start, theta_range)
