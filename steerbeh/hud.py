from os import path
import os
from pygame import Surface, font, mixer


class Hud:
    def __init__(self):
        self.assets_path = path.abspath('assets')
        fontpath = path.join(self.assets_path,
                             'fonts/JetBrainsMonoNL-Regular.ttf')
        self.font = font.SysFont(fontpath, 16)
        self.damage_snd = mixer.Sound(
            path.join(self.assets_path, 'sounds/hit1.ogg'))
        self.fps_label = None
        self.fps(0.)

    def fps(self, fps: float):
        txt = f'{str(int(fps))} fps'
        self.fps_label = self.font.render(txt, 1, (0, 0, 0))

    def play_damage(self):
        self.damage_snd.play()

    def render(self, sf: Surface):
        sf.blit(self.fps_label, (10, 10))
