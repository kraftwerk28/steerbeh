from pygame.math import Vector2 as Vec2
import sys
from .entities.base import BaseEntity
import os
import random


SCREEN_SIZE = Vec2(1000, 700)


def launch():
    import pygame as pg

    pos = Vec2(SCREEN_SIZE.x // 2, SCREEN_SIZE.y // 2)
    vel = Vec2(10, 10)
    mouse_pos = Vec2(pos)

    screen = pg.display.set_mode((int(SCREEN_SIZE.x), int(SCREEN_SIZE.y)))

    # arrow = pg.image.load('assets/arrow.png').convert_alpha()
    # arrow_rect = arrow.get_rect()
    entities = [
        BaseEntity(Vec2(random.randint(10, SCREEN_SIZE[0] - 10),
                        random.randint(10, SCREEN_SIZE[1] - 10)))
        for _ in range(100)
    ]

    running = True

    clk = pg.time.Clock()

    while running:
        clk.tick(60)
        screen.fill((255, 255, 255))

        # pg.draw.polygon(screen, (0, 0, 0, 0),
        #                 [(10, 10), (50, 30), (20, 80)], 10)

        # hw, hh = arrow_rect.w / 2, arrow_rect.h / 2
        # if pos.x < -hw or pos.x + hw > SCREEN_SIZE.x:
        #     vel.x *= -1
        # if pos.y < -hh or pos.y + hh > SCREEN_SIZE.y:
        #     vel.y *= -1

        # ang = vel.angle_to(Vec2(0, 1))
        # sf = pg.transform.rotate(arrow, ang)

        for e in entities:
            e.update(clk.get_time())
            e.steer(entities=entities, positions=[mouse_pos])
            e.render(screen)
        pg.display.flip()

        for evt in pg.event.get():
            if (evt.type == pg.QUIT
                    or evt.type == pg.KEYDOWN and evt.key == pg.K_ESCAPE):
                running = False
            if evt.type == pg.MOUSEMOTION:
                mouse_pos = Vec2(evt.pos)
