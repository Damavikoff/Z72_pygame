from typing import Callable
import pygame
from pygame.surface import Surface
from .c_text import Text
from ..defaults import ALIGN_LEFT

# DEF_COLOR = (200, 144, 25)
DEF_COLOR = (220, 184, 45)

class Caption:
  def __init__(self, text: str, align = ALIGN_LEFT, size = 24, actions: dict[int, Callable] = None, center: tuple[int] = None) -> None:
    self.image = Text(text = text, size = size, color = DEF_COLOR, alignment = align, paddings = (20, 0, 20, 0))
    self.rect = self.image.get_rect()
    if center:
      self.rect.center = center
    else:
      self.rect.topleft = (0, 0)
    w, h = self.image.get_size()
    pygame.draw.line(self.image, DEF_COLOR, (0, 1), (w, 1))
    pygame.draw.line(self.image, DEF_COLOR, (0, h - 1), (w, h - 1))
    self.actions = actions or {}


  def draw(self, target: Surface):
    target.blit(self.image, self.rect)

  def run(self, key: int):
    if key in self.actions:
      action = self.actions[key][0]
      args = self.actions[key][1]
      if callable(action):
        action(*args)