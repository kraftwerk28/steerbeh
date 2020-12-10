from dataclasses import dataclass
import json
from pygame.math import Vector2 as Vec2


@dataclass
class GameCfg:
    world_size: Vec2
    screen_size: Vec2
    hares: int = 10
    wolves: int = 4
    llamas: int = 8
    fps: int = 30

    @staticmethod
    def load(path):
        try:
            with open(path) as f:
                d = json.load(f)
        except:
            d = {}
        wx, wy = d.get('world_size', (1500, 1500))
        sx, sy = d.get('screen_size', (1000, 800))
        d.update({'world_size': Vec2(wx, wy), 'screen_size': Vec2(sx, sy)})
        return GameCfg(**d)
