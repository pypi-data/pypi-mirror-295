from ..game_object import GameObject, Prefab
import pygame as pg

class SceneData:
    name: str
    prefabs: list[Prefab]
    
    def __init__(self, name: str):
        self.name = name

class Scene:

    objects: list[GameObject]
    
    def __init__(self, data: SceneData | None = None):
        self.data = data

    def update(self):
        for i in self.objects:
            i.update()
    
    def draw(self, display: pg.Surface):
        for i in self.objects:
            i.draw(display)
