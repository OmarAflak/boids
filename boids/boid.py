import math
from dataclasses import dataclass
from boids.point import Point
from boids.obstacle import Obstacle


@dataclass
class Boid:
    MAX_VELOCITY = 6
    MAX_STEERING = 0.2
    REACTION_SPEED = 5
    SEPARATION_THRESHOLD = 30

    position: Point = Point()
    velocity: Point = Point()
    acceleration: Point = Point()

    def update(self, neighbors: 'list[Boid]', obstacles: 'list[Obstacle]'):
        new_acceleration = Point()
        new_acceleration += self._get_update_from_neighbors(neighbors)
        new_acceleration += self._get_update_from_obstacles(obstacles)
        self.acceleration = new_acceleration
        self._update()

    def vertices(self) -> 'tuple[Point, Point, Point]':
        direction = self.velocity.unit()
        normal = Point(-direction.y, direction.x)
        return (
            self.position + 8.0 * direction,
            self.position - 5.0 * direction + 3 * normal,
            self.position - 5.0 * direction - 3 * normal
        )

    def copy(self) -> 'Boid':
        return Boid(
            self.position.copy(),
            self.velocity.copy(),
            self.acceleration.copy()
        )

    def _get_update_from_neighbors(self, neighbors: 'list[Boid]') -> Point:
        if not neighbors:
            return Point()

        n = float(len(neighbors))
        new_acceleration = Point()
        avg_velocity = sum([n.velocity for n in neighbors], Point()) / n
        avg_position = sum([n.position for n in neighbors], Point()) / n

        # follow random boid when all directions cancel out
        if avg_velocity.is_zero():
            avg_velocity = neighbors[0].velocity

        # alignment
        alignment = avg_velocity
        alignment.set_length(Boid.REACTION_SPEED)
        alignment -= self.velocity
        alignment.limit_length(Boid.MAX_STEERING)
        new_acceleration += alignment

        # cohesion
        cohesion = avg_position - self.position
        cohesion.set_length(Boid.REACTION_SPEED)
        cohesion -= self.velocity
        cohesion.limit_length(Boid.MAX_STEERING)
        new_acceleration += cohesion

        # separation
        distance = (self.position - avg_position).length()
        separation = Point()
        if distance < Boid.SEPARATION_THRESHOLD:
            separation = self.position - avg_position
            separation.set_length(Boid.REACTION_SPEED)
            separation -= self.velocity
            separation.limit_length(Boid.MAX_STEERING)
        new_acceleration += separation

        return new_acceleration

    def _get_update_from_obstacles(self, obstacles: 'list[Obstacle]') -> Point:
        repulsion = Point()
        for obstacle in obstacles:
            force = obstacle.position - self.position
            distance = force.length()
            force = force.rotate(math.pi / 2)
            force.set_length(obstacle.repulsion / distance)
            repulsion.limit_length(Boid.MAX_STEERING)
            repulsion += force

        return repulsion

    def _update(self):
        self.position += self.velocity
        self.velocity += self.acceleration
        self.velocity.limit_length(Boid.MAX_VELOCITY)
