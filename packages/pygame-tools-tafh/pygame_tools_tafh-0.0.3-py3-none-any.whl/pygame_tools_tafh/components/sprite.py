import pygame

from ..game_object import Component
from pygame import Surface

class SpriteComponent(Component):

    def __init__(self, sprite_name: str, size: tuple[int, int]) -> None:
        super().__init__()

        self.size = size
        self.texture = pygame.image.load("./sprites/" + sprite_name).convert_alpha()

    def draw(self, display: Surface):
        blitImage = self.texture

        cropped = pygame.Surface(self.size)
        cropped.blit(blitImage, (0, 0))

        angle = self.game_object.transform.angle.get()
        scale = self.game_object.transform.scale

        if angle != 0:
            cropped = pygame.transform.rotate(cropped, angle)

        if scale != 1:
            cropped = pygame.transform.scale_by(cropped, scale)

        rect = cropped.get_rect(center=self.game_object.transform.position.as_tuple())

        pygame.draw.rect(display, (255, 0, 0), rect, 1)
        display.blit(blitImage, rect)
    