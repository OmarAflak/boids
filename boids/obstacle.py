from dataclasses import dataclass
from geometry.point import Point
from quadtree.locatable import Locatable


@dataclass
class Obstacle(Locatable):
    position: Point
    repulsion: float

    def get_x(self) -> float:
        return self.position.x

    def get_y(self) -> float:
        return self.position.y
