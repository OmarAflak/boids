import math
from boids.boid import Boid
from boids.obstacle import Obstacle
from geometry.point import Point
from geometry.box import Box
from quadtree.quadtree import QuadTree


class World:
    PERCEPTION_RADIUS = 50
    PERCEPTION_ANGLE = math.pi / 3

    def __init__(self, width: int, height: int, number_of_boids: int):
        self.width = width
        self.height = height
        self.box = Box.create(0, 0, width, height)
        self.boids: QuadTree[Boid] = QuadTree(self.box)
        for _ in range(number_of_boids):
            self.boids.add(
                Boid(
                    Point.random(range(width), range(height)),
                    Point.random(range(-5, 5, 2), range(-5, 5, 2))
                )
            )
        self.obstacles: QuadTree[Obstacle] = QuadTree(self.box)
        for i in range(0, width + 1, 150):
            for j in range(0, height + 1, 150):
                self.obstacles.add(Obstacle(Point(i, j), 20))

    def update(self):
        all_boids = self.boids.all()

        # update based on snapshot of current state
        copies = self.boids.copy(Boid.copy)

        for boid in all_boids:
            self.boids.remove(boid)
            boid_position = Point(boid.position.x, boid.position.y)

            neighbors = copies.get_in_circle(
                boid_position,
                World.PERCEPTION_RADIUS
            )

            if boid in neighbors:
                neighbors.remove(boid)

            visible_obstacles = [
                obstacle
                for obstacle in self.obstacles.get_in_circle(
                    boid_position,
                    2 * World.PERCEPTION_RADIUS
                )
                if abs(
                    boid.velocity.angle_to(obstacle.position - boid.position)
                ) <= World.PERCEPTION_ANGLE / 2
            ]

            boid.update(neighbors, visible_obstacles)
            boid.position.bound(0, self.width, 0, self.height)
            self.boids.add(boid)
