from .base import Base, BaseEntity
from pygame.math import Vector2 as Vec2
from pygame import draw, Surface


class Projectile(Base):
    speed_multiplier = 3

    def __init__(self, source: BaseEntity):
        new_vel = source.vel * self.speed_multiplier
        super().__init__(Vec2(source.pos), new_vel, Vec2(source.acc))

    def render(self, sf: Surface):
        pos = (self.pos.x, self.pos.y)
        draw.circle(sf, (255, 255, 255), pos, 5)
