from pygame.math import Vector2 as Vec2
from typing import List
from pygame import Surface, draw, SRCALPHA, Rect
from .entities.base import BaseEntity
from .constants import WORLD_BORDER_COLOR
from .utils import rand_vec2


class World:
    def __init__(self, screen_size: Vec2, world_size=Vec2(100, 100)):
        self.screen_size = Vec2(screen_size)
        self.screen_half_vec = Vec2(screen_size.x // 2, screen_size.y // 2)
        self.world_size = Vec2(world_size)
        self.offset_vec = Vec2()
        self.center_vec = Vec2()
        self.pointer_dir = Vec2(0, 1)
        self.bound_rect = Rect(0, 0, world_size.x, world_size.y)

    def center_at(self, pos: Vec2):
        self.center_vec = pos
        self.offset_vec = pos - self.screen_half_vec

    def set_pointer_pos(self, pos: Vec2):
        self.pointer_dir = pos - self.screen_half_vec

    def get_pointer_steer_vec(self):
        return self.center_vec + self.pointer_dir

    def render(self, sf: Surface, entities: List[BaseEntity] = []):
        rect_sf = Surface((self.world_size.x, self.world_size.y), SRCALPHA)
        rect = Rect(0, 0, self.world_size.x, self.world_size.y)
        draw.rect(rect_sf, WORLD_BORDER_COLOR, rect, width=10)
        for entity in entities:
            entity.render(rect_sf)

        sf.blit(rect_sf, -self.offset_vec)

    def rand_pos(self) -> Vec2:
        return rand_vec2(self.world_size)
