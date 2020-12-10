from os import path
import os
from pygame import Surface, font, mixer


class Hud:
    def __init__(self):
        self.assets_path = path.abspath('assets')
        fontpath = path.join(self.pth('fonts/JetBrainsMonoNL-Regular.ttf'))
        self.font = font.SysFont(fontpath, 16)
        self.damage_snd = mixer.Sound(self.pth('sounds/hit1.ogg'))
        self.bow_snd = mixer.Sound(self.pth('sounds/bow.ogg'))
        self.fall_snd = mixer.Sound(self.pth('sounds/fallbig.ogg'))
        self.fps_label = None
        self.fps(0.)

    def fps(self, fps: float):
        txt = f'{str(int(fps))} fps'
        self.fps_label = self.font.render(txt, 1, (255, 255, 255))

    def play_damage(self):
        self.damage_snd.play()

    def play_bow(self):
        self.bow_snd.play()

    def play_fall(self):
        self.fall_snd.play()

    def pth(self, *parts):
        return path.join(self.assets_path, *parts)

    def render(self, sf: Surface):
        sf.blit(self.fps_label, (10, 10))
