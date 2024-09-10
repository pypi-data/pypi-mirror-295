from dataclasses import dataclass
from decimal import getcontext

# global setting
getcontext().prec = 2


@dataclass
class Point2D:
    x: float
    y: float
