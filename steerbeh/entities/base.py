import math
import random
from typing import List
from pygame.math import Vector2 as Vec2
from pygame import Surface, draw, transform, SRCALPHA, Rect
from ..utils import get_avoid_rate
# from ..world import World

ARROW_PTS = [(0, 20), (10, 0), (20, 20), (10, 14)]
ANG_VEC = Vec2(0, -1)


class Base:
    def __init__(self,
                 pos: Vec2,
                 vel: Vec2 = Vec2(1, 1),
                 acc: Vec2 = Vec2(0, 0),
                 size: int = 10):
        self.pos = pos
        self.vel = vel
        self.acc = acc
        self.size = size
        self.hitbox = Rect(self.pos.x, self.pos.x, float(size), float(size))
        self.update_hitbox()

    def update_hitbox(self):
        hs = self.size // 2
        self.hitbox = Rect(self.pos.x - hs, self.pos.y - hs, self.size,
                           self.size)

    def update(self, dt: float):
        self.vel += self.acc * dt
        self.pos += self.vel * dt
        self.update_hitbox()


class BaseEntity(Base):
    # When to start slowing down if near target
    slowstart_radius = 80
    border_notice_distance = 100
    seek_notice_distance = 200
    flee_notice_distance = 200

    max_speed = 0.05
    flee_max_speed = 0.1

    target_follow_factor = 0.01
    target_flee_factor = 0.02
    wandering_factor = 0.01
    border_avoid_factor = 1

    def __init__(self,
                 pos: Vec2,
                 vel: Vec2 = Vec2(1, 1),
                 acc: Vec2 = Vec2(0, 0),
                 max_speed=None,
                 steer_force=None,
                 color=None):
        super().__init__(pos, vel, acc)
        self.arrow_color = color or (0, 0, 0)
        self.steering_vec = Vec2()
        self.wandering_vec = Vec2(0, 1)
        self.current_max_speed = BaseEntity.max_speed

    def seek_target(self, pos: Vec2):
        if pos.distance_squared_to(self.pos) <= self.seek_notice_distance**2:
            v = (pos - self.pos).normalize() * self.target_follow_factor
            self.steering_vec += v

    def flee_target(self, pos: Vec2):
        if pos.distance_squared_to(self.pos) <= self.flee_notice_distance**2:
            self.current_max_speed = self.flee_max_speed
            v = (self.pos - pos).normalize() * self.target_flee_factor
            self.steering_vec += v
        else:
            self.current_max_speed = self.max_speed

    def wander(self):
        rot = self.wandering_vec.rotate(random.randint(-45, 45))
        self.wandering_vec = rot
        self.steering_vec += self.wandering_vec * self.wandering_factor

    def avoid_borders(self, world):
        avoid_vec = get_avoid_rate(self.pos, self.vel, world.world_size,
                                   self.border_notice_distance)
        self.steering_vec += avoid_vec * self.border_avoid_factor

    def update(self, dt: float):
        self.vel += self.acc * dt
        self.vel = (self.vel + self.steering_vec).normalize()
        if self.vel.length_squared() > self.current_max_speed**2:
            self.vel = self.vel.normalize() * self.current_max_speed
        self.pos += self.vel * dt
        self.update_hitbox()
        self.steering_vec = Vec2()

    def apply_behavior(self, method, entities: List['BaseEntity']):
        for entity in entities:
            if entity == self:
                continue
            method(entity.pos)

    def collision(self, entities: List['Base']) -> List['BaseEntity']:
        rects = [e.hitbox for e in entities if e != self]
        indices = self.hitbox.collidelistall(rects)
        return [entities[i] for i in indices]

    def render(self, sf: Surface) -> Surface:
        arrow_sf = Surface((20, 20), SRCALPHA)
        draw.polygon(arrow_sf, self.arrow_color, ARROW_PTS)
        final_sf = transform.rotate(arrow_sf, self.vel.angle_to(ANG_VEC))
        sf.blit(final_sf, (self.pos.x - 10, self.pos.y - 10))
