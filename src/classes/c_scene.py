import pygame
from ..defaults import SCENE_IMAGES, SCENE_SIZE
from pygame.sprite import Sprite
from pygame.surface import Surface
from pygame.image import load
from pygame.transform import scale

class Scene(Sprite):
  def __init__(self, size: tuple[int], images: list[str]) -> None:
    super().__init__()
    self.shift = 0
    self.scale = scale
    self.size = size
    self.frames = []
    self.set_frames(images)
    self.image = Surface(self.size, pygame.SRCALPHA, 32).convert_alpha()
    self.rect = self.image.get_rect()
    self.render_scene()

  def set_frames(self, images: list[str]) -> None:
    frames = []
    w, h = self.size
    for i in images:
      image = load(i).convert_alpha()
      i_w, i_h = image.get_size()
      ratio = w / i_w
      if h > w:
        ratio = h / i_h
      size = [v * ratio for v in image.get_size()]
      image = scale(image, size)
      surface = Surface(self.size, pygame.SRCALPHA, 32).convert_alpha()
      surface.blit(image, (0, 0), (0, i_h * ratio - h, *self.size))
      frames.append(surface)
    self.frames = frames

  def render_scene(self) -> None:
    self.image.fill((0, 0, 0, 0))
    for i in self.frames:
      self.image.blit(i, (0, 0))
