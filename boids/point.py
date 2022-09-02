import math
from dataclasses import dataclass
from random import randrange
from typing import Optional


@dataclass
class Point:
    x: float = 0
    y: float = 0

    def length(self) -> float:
        return (self.x ** 2 + self.y ** 2) ** 0.5

    def unit(self) -> 'Point':
        return self / self.length()

    def distance_to(self, other: 'Point') -> float:
        return (self - other).length()

    def angle_to(self, other: 'Point') -> float:
        return math.atan2(other.y, other.x) - math.atan2(self.y, self.x)

    def rotate(
        self,
        angle: float,
        around: Optional['Point'] = None
    ) -> 'Point':
        around = around or Point()
        tmp = self - around
        return around + Point(
            tmp.x * math.cos(angle) - tmp.y * math.sin(angle),
            tmp.x * math.sin(angle) + tmp.y * math.cos(angle)
        )

    def dot(self, other: 'Point') -> float:
        return self.x * other.x + self.y * other.y

    def bound(self, x_min: float, x_max: float, y_min: float, y_max: float):
        if self.x > x_max:
            self.x = x_min
        if self.x < x_min:
            self.x = x_max
        if self.y > y_max:
            self.y = y_min
        if self.y < y_min:
            self.y = y_max

    def set_length(self, length: float):
        factor = length / self.length()
        self.x *= factor
        self.y *= factor

    def limit_length(self, max_length: float):
        length = self.length()
        if length > max_length:
            self.set_length(max_length)

    def is_zero(self) -> bool:
        return self.x == 0 and self.y == 0

    def copy(self) -> 'Point':
        return Point(self.x, self.y)

    def __add__(self, other: 'Point') -> 'Point':
        return Point(self.x + other.x, self.y + other.y)

    def __sub__(self, other: 'Point') -> 'Point':
        return Point(self.x - other.x, self.y - other.y)

    def __mul__(self, other: float) -> 'Point':
        return Point(self.x * other, self.y * other)

    def __rmul__(self, other: float) -> 'Point':
        return self * other

    def __truediv__(self, other: float) -> 'Point':
        return self * (1 / other)

    def __neg__(self) -> 'Point':
        return Point() - self

    @classmethod
    def random(cls, x_range: range, y_range: range) -> 'Point':
        return Point(
            randrange(x_range.start, x_range.stop, x_range.step),
            randrange(y_range.start, y_range.stop, y_range.step)
        )
