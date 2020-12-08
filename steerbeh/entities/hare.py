from typing import List
from .base import BaseEntity


class Hare(BaseEntity):
    flee_radius = 100

    def __init__(self, *args):
        super().__init__(*args)
        self.arrow_color = (255, 0, 255)
