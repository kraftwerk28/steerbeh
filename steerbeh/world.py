from pygame.math import Vector2 as Vec2
from typing import List
from pygame import Surface, draw, SRCALPHA
from .entities.hunter import Hunter


class World:
    def __init__(self, screen_size: Vec2, world_size=Vec2(100, 100)):
        self.screen_size = Vec2(screen_size)
        self.screen_half_vec = Vec2(screen_size.x // 2, screen_size.y // 2)
        self.world_size = Vec2(world_size)
        self.offset_vec = Vec2()

    def center_at(self, player: Hunter):
        self.offset_vec = player.pos - self.screen_half_vec

    def render(self, sf: Surface, entities: List[EntityBase] = []):
        rect_sf = Surface((self.world_size.x, self.world_size.y), SRCALPHA)
        draw.rect(rect_sf, (0, 0, 0), width=10)
        sf.blit(rect_sf, -self.offset_vec)
        # Render entities
