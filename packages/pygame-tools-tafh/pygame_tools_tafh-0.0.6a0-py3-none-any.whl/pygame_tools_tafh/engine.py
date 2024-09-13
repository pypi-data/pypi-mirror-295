from .events import events
from .scene_manager import Scene
from .game_object import GameObject
import pygame as pg
import logging


class Engine:

    scenes: list[Scene]
    logger: logging.Logger
    scene: Scene
    display: pg.Surface

    def __init__(self, app_name: str, resolution: tuple[int, int] = (800, 600)):
        self.app_name = app_name
        self.logger = logging.getLogger()
        self.logger.setLevel(logging.INFO)
        handler = logging.StreamHandler()
        handler.setFormatter(logging.Formatter("[%(levelname)s][%(name)s]: %(message)s"))
        self.logger.addHandler(handler)
        self.init(resolution)

    def register(self, scene: Scene):
        self.scenes.append(scene)

    def init(self, resolution: tuple[int, int] = (800, 600)):
        pg.init()
        pg.font.init()
        logging.basicConfig()
        self.display = pg.display.set_mode(resolution)
        pg.display.set_caption(self.app_name)
        logging.info("Game initialized.")

    def run(self):
        try:
            self.cycle()
        except Exception as e:
            logging.critical(e.with_traceback(None))
            exit(1)

    def event_processing(self, event: pg.event.Event):
        if event.type == pg.QUIT:
            logging.info("Quitting")
            exit()

    def iteration(self):
        events.set(pg.event.get())
        
        for event in events.get():
            self.event_processing(event)
        
        for i in GameObject.objects:
            i.update()

        for i in GameObject.objects:
            i.draw(self.display)

        pg.display.flip()
        
    def cycle(self):
        while True:
            self.iteration()
            
