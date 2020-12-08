from .base import BaseEntity
from .hare import Hare
from .hunter import Hunter
from .llama import Llama


class Wolf(BaseEntity):
    killable_entities = [Hare, Hunter, Llama]

    # seek_notice_distance = 500

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.arrow_color = (180, 180, 180)
