import numpy as np
import pyglet

from boids.boid import Boid
from boids.point import Point
from boids.obstacle import Obstacle


window = pyglet.window.Window(600, 600, caption="Boids")
batch = pyglet.graphics.Batch()

boids = [
    Boid(
        Point.random(range(window.width), range(window.height)),
        Point.random(range(-5, 5, 2), range(-5, 5, 2))
    )
    for _ in range(100)
]

obstacles = [
    Obstacle(Point(i, j), 20)
    for i in range(0, window.width + 1, 150)
    for j in range(0, window.height + 1, 150)
]

perception_radius = 50
perception_angle = np.pi / 3


def create_triangles(
    triangles: 'list[tuple[Point, Point, Point]]',
    batch: pyglet.shapes.Batch
) -> 'list[pyglet.shapes.Triangle]':
    return [
        pyglet.shapes.Triangle(p1.x, p1.y, p2.x, p2.y, p3.x, p3.y, batch=batch)
        for p1, p2, p3 in triangles
    ]


def create_points(
    points: 'list[Point]',
    batch: pyglet.shapes.Batch
) -> 'list[pyglet.shapes.Circle]':
    return [
        pyglet.shapes.Circle(p.x, p.y, 2, color=(255, 0, 0), batch=batch)
        for p in points
    ]


def update_boids(value):
    # update based on snapshot of current state
    copies = [boid.copy() for boid in boids]

    for boid in boids:
        neighbors = []
        for b in copies:
            if b == boid:
                continue

            if b.position.distance_to(boid.position) > perception_radius:
                continue

            neighbors.append(b)

        visible_obstacles = []
        for obstacle in obstacles:
            if obstacle.position.distance_to(boid.position) > 2 * perception_radius:
                continue

            target = obstacle.position - boid.position
            if abs(boid.velocity.angle_to(target)) > perception_angle / 2:
                continue

            visible_obstacles.append(obstacle)

        boid.update(neighbors, visible_obstacles)
        boid.position.bound(0, window.width, 0, window.height)


@window.event
def on_draw():
    _1 = create_triangles([boid.vertices() for boid in boids], batch)
    _2 = create_points([obstacle.position for obstacle in obstacles], batch)
    window.clear()
    batch.draw()


pyglet.clock.schedule_interval(update_boids, 0.01)
pyglet.app.run()
