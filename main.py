import pyglet
from geometry.point import Point
from boids.world import World


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


window = pyglet.window.Window(600, 600, caption="Boids")
batch = pyglet.graphics.Batch()
world = World(window.width, window.height, number_of_boids=100)
boids = world.boids.all()
obstacles = world.obstacles.all()
boid_shapes = create_triangles([boid.vertices() for boid in boids], batch)
obstacle_shapes = create_points([obstacle.position for obstacle in obstacles], batch)


@window.event
def on_draw():
    boid_vertices = [boid.vertices() for boid in boids]
    for shape, p in zip(boid_shapes, boid_vertices):
        shape.position = p[0].x, p[0].y, p[1].x, p[1].y, p[2].x, p[2].y

    obstacle_vertices = [obstacle.position for obstacle in obstacles]
    for shape, p in zip(obstacle_shapes, obstacle_vertices):
        shape.position = p.x, p.y

    window.clear()
    batch.draw()


pyglet.clock.schedule_interval(lambda _: world.update(), 0.001)
pyglet.app.run()
