from typing import List
from pygame.math import Vector2 as Vec2
from .base import BaseEntity
from ..utils import centroid


class Llama(BaseEntity):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.arrow_color = (127, 100, 255)

    def flock(self, llamas: List['Llama']):
        pts = []
        sep_vec = Vec2()
        for llama in llamas:
            dst = self.pos.distance_squared_to(llama.pos)
            if llama == self or dst > self.flock_notice_distance**2:
                continue
            pts.append(llama.pos)
            sep_vec += self.pos - llama.pos
        away_vec = sep_vec * self.flock_group_factor
        group_vec = centroid(pts) - self.pos
        self.steering_vec += away_vec + group_vec
