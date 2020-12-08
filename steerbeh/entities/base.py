from typing import List
from pygame.math import Vector2 as Vec2
from pygame import Surface, draw, transform, SRCALPHA
from ..world import World

ARROW_PTS = [(0, 20), (10, 0), (20, 20), (10, 14)]
ANG_VEC = Vec2(0, -1)


class BaseEntity:
    def __init__(self, pos: Vec2, vel: Vec2 = Vec2(1, 0),
                 acc: Vec2 = Vec2(0, 0),
                 max_speed=None, steer_force=None, color=None):
        self.pos = pos
        self.vel = vel
        self.acc = acc
        self.max_speed = max_speed or 0.1
        self.steer_force = 0.006
        self.slowstart_radius = 80
        self.fill_color = color or (0, 0, 0)
        self.steer_vec = Vec2(0, 0)

    def update(self, dt: float):
        self.vel += self.acc * dt
        self.pos += self.vel * dt
        self.vel = (self.vel + self.steer_vec).normalize() * self.max_speed

        # next_vel = (self.vel + steer_vec).normalize()

        # dst = dir_vec.length()
        # if dst < self.slowstart_radius:
        #     k = dst / self.slowstart_radius
        #     self.vel = next_vel * k * self.max_speed
        # else:
        #     self.vel = next_vel * self.max_speed

    def __str__(self):
        return ''

    def steer(self, entities: List['BaseEntity'] = [],
              positions=List[Vec2], world: World = None) -> Vec2:
        v = Vec2(0, 0)
        for entity in entities:
            if entity == self:
                continue
            v += self.steer_pos(entity.pos)
        for pos in positions:
            v += self.steer_pos(pos)
        self.steer_vec = v

    def steer_pos(self, pos: Vec2) -> Vec2:
        dir_vec = Vec2(pos - self.pos)
        des_vel = dir_vec.normalize()
        return (des_vel - self.vel) * self.steer_force

    def render(self, sf: Surface) -> Surface:
        arrow_sf = Surface((20, 20), SRCALPHA)
        rect = draw.polygon(arrow_sf, self.fill_color, ARROW_PTS)
        final_sf = transform.rotate(arrow_sf, self.vel.angle_to(ANG_VEC))
        sf.blit(final_sf, (self.pos.x - 10, self.pos.y - 10))
