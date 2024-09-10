import abc
import os
from typing import List
from pyturtle.shapes.point import Point2D


class Shape(metaclass=abc.ABCMeta):
    def __init__(self, num_coordinates):
        self.coordinates: List[Point2D] = []
        self.num_coordinates: int = num_coordinates

    @abc.abstractmethod
    def set_coordinates(self):
        """This can be overridden by subclasses for specific behavior."""
        # self.coordinates = []
        pass

    def get_coordinates(self):
        return self.coordinates

    def draw(self, turtle_instance):
        """Draw the shape using the provided Turtle instance."""
        turtle_instance.penup()
        if self.coordinates:
            turtle_instance.goto(self.coordinates[0].x, self.coordinates[0].y)
            turtle_instance.pendown()
            for coord in self.coordinates:
                turtle_instance.goto(coord.x, coord.y)
            # turtle_instance.goto(self.coordinates[0].x, self.coordinates[0].y)  # Close the shape
        turtle_instance.penup()

    @abc.abstractmethod
    def translate_x(self, x_shift):
        pass

    @abc.abstractmethod
    def translate_y(self, y_shift):
        pass

    @abc.abstractmethod
    def translate_xy(self, x_shift, y_shift):
        pass

    @abc.abstractmethod
    def rotate(self, degrees):
        pass

    @abc.abstractmethod
    def get_slice(self, step_one, step_two):
        pass

    @abc.abstractmethod
    def get_random_slice(self):
        pass

    def _update_coordinate(self, key, value):
        self.coordinates[key] = value

    def get_coordinate(self, key):
        return self.coordinates[key]

    def get_coordinates(self):
        return self.coordinates
