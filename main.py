import pyglet
from boids.point import Point
from boids.world import World


window = pyglet.window.Window(600, 600, caption="Boids")
batch = pyglet.graphics.Batch()
world = World(window.width, window.height, 100)


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


def update(value):
    world.update()


@window.event
def on_draw():
    _1 = create_triangles([boid.vertices() for boid in world.boids], batch)
    _2 = create_points([obstacle.position for obstacle in world.obstacles], batch)
    window.clear()
    batch.draw()


pyglet.clock.schedule_interval(update, 0.01)
pyglet.app.run()
