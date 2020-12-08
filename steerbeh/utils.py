from typing import Tuple, List
import random
from pygame.math import Vector2 as Vec2


def rand_vec2(world_size: Vec2) -> Vec2:
    return Vec2(random.randint(0, world_size.x),
                random.randint(0, world_size.y))


def trunc_vec2(vec: Vec2, max_length: float) -> Vec2:
    return vec.normalize() * max_length


def vec2inttup(vec: Vec2) -> Tuple[int, int]:
    return (int(vec.x), int(vec.y))


def get_avoid_rate(pos: Vec2, vel: Vec2, world_size: Vec2,
                   avoid_distance: int) -> Vec2:
    x, y = 0, 0
    px, py = pos.x, pos.y
    vx, vy = vel.x, vel.y

    if px < avoid_distance and vx < 0:
        x = -(1 - px / avoid_distance) * vx
    elif px > world_size.x - avoid_distance and vx > 0:
        x = -((px - world_size.x) / avoid_distance + 1) * vx

    if py < avoid_distance and vy < 0:
        y = -(1 - py / avoid_distance) * vy
    elif py > world_size.y - avoid_distance and vy > 0:
        y = -((py - world_size.y) / avoid_distance + 1) * vy

    # a_2, a = avoid_distance * 2, avoid_distance
    # cx, cy = a_2, a_2
    # if px < cx and py < cy:
    #     if pos.distance_squared_to(Vec2(cx, cy)) >= avoid_distance**2:
    #         x, y = (cx - px - a) / a, (cy - py - a) / a
    # cx = world_size.x - a_2
    # if px > cx and py < cy:
    #     if pos.distance_squared_to(Vec2(cx, cy)) >= avoid_distance**2:
    #         x, y = (cx - px) / a, (cy - py) / a
    # cy = world_size.y - a_2
    # if px > cx and py > cy:
    #     if pos.distance_squared_to(Vec2(cx, cy)) >= avoid_distance**2:
    #         x, y = (cx - px) / a, (cy - py) / a
    # cx = a_2
    # if px < cx and py > cy:
    #     if pos.distance_squared_to(Vec2(cx, cy)) >= avoid_distance**2:
    #         x, y = (cx - px) / a, (cy - py) / a

    return Vec2(x, y)


def centroid(points: List[Vec2]) -> Vec2:
    x = sum(v.x for v in points) / len(points)
    y = sum(v.y for v in points) / len(points)
    return Vec2(x, y)
