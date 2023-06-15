from pygame import Surface


class Transform:
    def __init__(self, x=0, y=0, *args, **kwargs):
        self._x = x
        self._y = y

    @property
    def x(self):
        return self._x

    @property
    def y(self):
        return self._y

    def translate(self, x, y):
        self._x += x
        self._y += y

    def setPosition(self, x: int, y: int):
        self._x = x
        self._y = y

    def __str__(self):
        return f"Transform[{self.x}, {self.y}]"


class GameObject:
    def __init__(self):
        self.transform = Transform()

    def draw(self, surface: Surface):
        pass

    def start(self):
        pass

    def __str__(self):
        return f"<{str(self.__class__)[8:-2]}({self.transform.x}, {self.transform.y})>"
