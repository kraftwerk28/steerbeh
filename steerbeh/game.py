import os
import sys
import random
from pygame.math import Vector2 as Vec2
import pygame as pg
from .entities import BaseEntity, Hunter
from .world import World
from .hud import Hud
from .entity_manager import EntityManager
from .utils import vec2inttup
from .constants import BACKGROUND_COLOR


class Game:
    fps = 30
    world_size = Vec2(800, 800)
    screen_size = Vec2(1000, 700)

    def __init__(self):
        pg.init()
        self.clock = pg.time.Clock()
        self.world = World(self.screen_size, self.world_size)
        self.screen = pg.display.set_mode(vec2inttup(self.screen_size))
        self.hud = Hud()
        self.entitymgr = EntityManager(self.world, self.hud)
        self.running = False

    def run(self):
        self.running = True
        while self.running and not self.entitymgr.hunter.died:
            self.hud.fps(self.clock.get_fps())

            self.update()
            self.render()
            self.fetch_events()
            self.clock.tick(self.fps)
        score = self.entitymgr.hunter.score
        print(f'You lost; score = {score}')

    def update(self):
        self.entitymgr.follow_mouse(self.world.get_pointer_steer_vec())
        self.world.center_at(self.entitymgr.hunter.pos)

        dt = self.clock.get_time()
        self.entitymgr.update(dt, self.world)

    def render(self):
        self.screen.fill(BACKGROUND_COLOR)
        self.world.render(self.screen, self.entitymgr.get_all_entities())
        self.hud.render(self.screen)
        pg.display.flip()

    def fetch_events(self):
        for evt in pg.event.get():
            if (evt.type == pg.QUIT
                    or evt.type == pg.KEYDOWN and evt.key == pg.K_ESCAPE):
                self.running = False
            if evt.type == pg.MOUSEMOTION:
                self.world.set_pointer_pos(Vec2(evt.pos))
            if evt.type == pg.MOUSEBUTTONDOWN:
                self.hud.play_bow()
                self.entitymgr.hunter_shoot()
