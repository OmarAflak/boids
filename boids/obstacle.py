from dataclasses import dataclass
from boids.point import Point


@dataclass
class Obstacle:
    position: Point
    repulsion: float
