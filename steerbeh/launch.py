from .entities.base import BaseEntity
from .utils.vec import Vec2


def launch():
    e = BaseEntity(Vec2.zero(), Vec2.zero(), Vec2.zero())
    print(e)
