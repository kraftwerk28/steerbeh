from typing import Tuple, List
import random
from pygame.math import Vector2 as Vec2
from math import copysign


def rand_vec2(world_size: Vec2) -> Vec2:
    return Vec2(random.randint(0, world_size.x),
                random.randint(0, world_size.y))


def trunc_vec2(vec: Vec2, max_length: float) -> Vec2:
    return vec.normalize() * max_length


def vec2inttup(vec: Vec2) -> Tuple[int, int]:
    return (int(vec.x), int(vec.y))


def get_avoid_rate_linear(pos: Vec2, vel: Vec2, world_size: Vec2,
                          avoid_distance: int) -> Vec2:
    x, y = 0, 0
    px, py = pos.x, pos.y
    vx, vy = vel.x, vel.y

    if px < avoid_distance and vx < 0:
        x = -vx
    elif px > world_size.x - avoid_distance and vx > 0:
        x = -vx

    if py < avoid_distance and vy < 0:
        y = -vy
    elif py > world_size.y - avoid_distance and vy > 0:
        y = -vy
    res = Vec2(x, y)
    if x != 0 or y != 0:
        res.normalize_ip()
    return res


def get_avoid_rate(pos: Vec2, vel: Vec2, world_size: Vec2,
                   avoid_distance: int) -> Vec2:
    x, y = 0, 0
    px, py = pos.x, pos.y
    vx, vy = vel.x, vel.y

    k = 0
    if px < avoid_distance and vx < 0:
        k = 1 - px / avoid_distance
        if vy > 0:
            x, y = vy, -vx
        else:
            x, y = -vy, vx
        # x = -(1 - px / avoid_distance) * vx
    elif px > world_size.x - avoid_distance and vx > 0:
        k = (px - world_size.x) / avoid_distance + 1
        if vy > 0:
            x, y = -vy, vx
        else:
            x, y = vy, -vx
        # x, y = vy, -vx
        # x = -((px - world_size.x) / avoid_distance + 1) * vx

    if py < avoid_distance and vy < 0:
        k = 1 - py / avoid_distance
        if vx > 0:
            x, y = -vy, vx
        else:
            x, y = vy, -vx
        # x, y = vy, -vx
        # y = -(1 - py / avoid_distance) * vy
    elif py > world_size.y - avoid_distance and vy > 0:
        k = (py - world_size.y) / avoid_distance + 1
        if vx > 0:
            x, y = vy, -vx
        else:
            x, y = -vy, vx
        # x, y = vy, -vx
        # y = -((py - world_size.y) / avoid_distance + 1) * vy
    res = Vec2(x, y)
    if res.length_squared() > 0:
        res = res.normalize() * k
        res.normalize_ip()
    return res


def centroid(points: List[Vec2]) -> Vec2:
    x = sum(v.x for v in points) / len(points)
    y = sum(v.y for v in points) / len(points)
    return Vec2(x, y)
