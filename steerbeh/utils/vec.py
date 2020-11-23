import math


class Vec2:
    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y

    def __add__(self, other: 'Vec2'):
        return Vec2(self.x + other.x, self.y + other.y)

    def __sub__(self, other: 'Vec2'):
        return Vec2(self.x - other.x, self.y - other.y)

    def __iadd__(self, other: 'Vec2'):
        return self + other

    def __iadd__(self, other: 'Vec2'):
        return self + other

    def __isub__(self, other: 'Vec2'):
        return self - other

    def __invert__(self):
        return Vec2(-self.x, -self.y)

    def __mul__(self, n: float) -> 'Vec2':
        return Vec2(self.x * n, self.y * n)

    def __truediv__(self, n: float) -> 'Vec2':
        return Vec2(self.x / n, self.y / n)

    def dot(self, other: 'Vec2') -> float:
        return self.x * other.x + self.y * other.y

    def len(self) -> float:
        return math.sqrt(self.x ** 2 + self.y ** 2)

    def norm(self):
        length = self.len()
        return Vec2(self.x / length, self.y / length)

    def __str__(self):
        return f'Vec2(x = {self.x}, y = {self.y})'

    @staticmethod
    def zero() -> 'Vec2':
        return Vec2(0., 0.)
