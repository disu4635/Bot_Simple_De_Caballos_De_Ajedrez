from pygame import Surface
from core.gameObject import GameObject


class Scene:
    def __init__(self):
        self.gameObjects: dict[str, GameObject] = {}

    def initGameObjects(self):
        pass

    def start(self):
        self.initGameObjects()
        for gameObject in self.gameObjects.values():
            gameObject.start()

    def update(self, events, keys):
        pass

    def draw(self, surface: Surface):
        for key, value in self.gameObjects.items():
            value.draw(surface)

    def getGameObject(self, name):
        if name in self.gameObjects:
            return self.gameObjects[name]
        print("GameObject not found")
        return None
