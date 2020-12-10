from pygame.math import Vector2 as Vec2
from typing import List
from pygame import Surface, draw, SRCALPHA, Rect
from .entities.base import BaseEntity
from .constants import WORLD_BORDER_COLOR
from .utils import rand_vec2


class World:
    grid_tiles = 8

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
        size_tup = (self.world_size.x, self.world_size.y)
        rect_sf = Surface(size_tup, SRCALPHA)
        grid_sf = Surface(size_tup, SRCALPHA)
        grid_sf.set_alpha(80)

        rect = Rect(0, 0, self.world_size.x, self.world_size.y)
        draw.rect(rect_sf, WORLD_BORDER_COLOR, rect, width=10)

        stepx = self.world_size.x / self.grid_tiles
        stepy = self.world_size.y / self.grid_tiles
        # Draw grid
        for i in range(1, self.grid_tiles // 2):
            px, py = round(i * stepx), round(i * stepy)
            rx = Rect(px, 0, self.world_size.x - px * 2, self.world_size.y)
            ry = Rect(0, py, self.world_size.x, self.world_size.y - py * 2)
            draw.rect(grid_sf, WORLD_BORDER_COLOR, rx, 1)
            draw.rect(grid_sf, WORLD_BORDER_COLOR, ry, 1)
        rcx = Rect(0, 0, self.world_size.x // 2, self.world_size.x)
        rcy = Rect(0, 0, self.world_size.y, self.world_size.y // 2)
        draw.rect(grid_sf, WORLD_BORDER_COLOR, rcx, 1)
        draw.rect(grid_sf, WORLD_BORDER_COLOR, rcy, 1)

        for entity in entities:
            entity.render(rect_sf)

        sf.blit(rect_sf, -self.offset_vec)
        sf.blit(grid_sf, -self.offset_vec)

    def rand_pos(self) -> Vec2:
        return rand_vec2(self.world_size)
