from ..utils.vec import Vec2


class BaseEntity:
    def __init__(self, pos: Vec2, vel: Vec2, acc: Vec2):
        self.pos = pos
        self.vel = vel
        self.acc = acc

    def update(self, dt: float):
        self.vel += self.acc * dt
        self.pos += self.vel * dt

    def __str__(self):
        return ''
