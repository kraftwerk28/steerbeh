from typing import List
import random
from pygame.math import Vector2 as Vec2
from .base import BaseEntity
from ..utils import centroid


class Llama(BaseEntity):
    separation_distance = 100
    flock_notice_distance = 200
    leader_probability = 0.5
    group_size = 3

    flock_group_factor = 0.03
    flock_separate_factor = 0.9

    def setup(self):
        self.arrow_color = (127, 100, 255)

    def flock(self, llamas: List['Llama']):
        pts = []
        flock_vec = Vec2()
        sep_vec = Vec2()
        current_group = 0

        for llama in llamas:
            if llama == self:
                continue
            dst = self.pos.distance_squared_to(llama.pos)
            if dst < self.separation_distance**2:
                sep_vec += self.pos - llama.pos

            if (dst < self.flock_notice_distance**2
                    and current_group < self.group_size - 1):
                current_group += 1
                pts.append(llama.pos)

        sep_vec_len = sep_vec.length()
        sep_mul = (1 - sep_vec_len / self.separation_distance)
        sep_mul *= self.flock_separate_factor
        if sep_vec.length_squared() > 0:
            sep_vec = sep_vec.normalize() * sep_mul

        if pts:
            center = centroid(pts)
            flock_vec = center - self.pos
            if flock_vec.length_squared() > 0:
                flock_vec = flock_vec.normalize() * self.flock_group_factor

        self.steering_vec += flock_vec + sep_vec
