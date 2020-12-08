from .base import BaseEntity


class Wolf(BaseEntity):
    # seek_notice_distance = 500

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.arrow_color = (180, 180, 180)
