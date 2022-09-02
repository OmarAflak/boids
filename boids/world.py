import math
from boids.boid import Boid
from boids.obstacle import Obstacle
from boids.point import Point


class World:
    PERCEPTION_RADIUS = 50
    PERCEPTION_ANGLE = math.pi / 3

    def __init__(self, width: int, height: int, number_of_boids: int):
        self.width = width
        self.height = height
        self.boids = [
            Boid(
                Point.random(range(width), range(height)),
                Point.random(range(-5, 5, 2), range(-5, 5, 2))
            )
            for _ in range(number_of_boids)
        ]
        self.obstacles = [
            Obstacle(Point(i, j), 20)
            for i in range(0, width + 1, 150)
            for j in range(0, height + 1, 150)
        ]

    def update(self):
        # update based on snapshot of current state
        copies = [boid.copy() for boid in self.boids]

        for boid in self.boids:
            neighbors = []
            for b in copies:
                if b == boid:
                    continue

                if b.position.distance_to(boid.position) > World.PERCEPTION_RADIUS:
                    continue

                neighbors.append(b)

            visible_obstacles = []
            for obstacle in self.obstacles:
                if obstacle.position.distance_to(boid.position) > 2 * World.PERCEPTION_RADIUS:
                    continue

                target = obstacle.position - boid.position
                if abs(boid.velocity.angle_to(target)) > World.PERCEPTION_ANGLE / 2:
                    continue

                visible_obstacles.append(obstacle)

            boid.update(neighbors, visible_obstacles)
            boid.position.bound(0, self.width, 0, self.height)
