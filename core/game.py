from typing import Type

import pygame

from core.errors import LoadSceneError
from core.scene import Scene


class Game:
    instance = None
    frameRate = 60

    def __init__(self, width, height, *args, **kwargs):
        Game.instance = self
        kwargs.setdefault("title", "No title")
        pygame.init()
        pygame.display.set_caption(kwargs.pop("title"))
        pygame.font.init()
        self.size = self.width, self.height = width, height
        self.screen = pygame.display.set_mode(self.size)
        self.scenes: list[Scene] = []
        self.scene = None
        self.clock = pygame.time.Clock()
        self.quitStatus = False
        self.pause = False

    def loadScene(self, scene=0):
        if (
            len(self.scenes) >= 0
            and scene < len(self.scenes)
            and isinstance(self.scenes[scene], Scene)
        ):
            self.scene = self.scenes[scene]
            self.scene.start()
        else:
            raise LoadSceneError("Error al cargar la escena")

    def run(self):
        self.loadScene()
        if isinstance(self.scene, Scene):
            while True:
                events = pygame.event.get()
                for event in events:
                    if event.type == pygame.QUIT:
                        self.quitGame()
                if self.quitStatus:
                    break
                self.scene.update(events, pygame.key.get_pressed())
                self.scene.draw(self.screen)
                pygame.display.update()
                self.clock.tick(self.frameRate)

    def quitGame(self):
        pygame.quit()
        self.quitStatus = True

    def addScene(self, scene: Scene):
        self.scenes.append(scene)
        return self

    def setupScenes(self, scenes: list[Type[Scene]]):
        self.scenes = [scene() for scene in scenes]
        return self
