from typing import List
from .base import BaseEntity


class Hare(BaseEntity):
    flee_radius = 100
    max_speed = 0.03
    flee_notice_distance = 100

    def setup(self):
        self.arrow_color = (255, 0, 255)
