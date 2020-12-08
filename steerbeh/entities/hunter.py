from .base import BaseEntity


class Hunter(BaseEntity):
    seek_notice_distance = 3000

    def setup(self):
        self.died = False
        self.arrow_color = (255, 255, 255)
        self.score = 0
