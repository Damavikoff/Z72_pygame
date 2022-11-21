import pygame
from pygame.sprite import Sprite
from pygame.surface import Surface
from ..defaults import FPS, LEFT, RIGHT, WHITESMOKE

class HealthBar(Sprite):
  def __init__(self, size: tuple[int] = None, color: tuple[int] = None, side = LEFT, max_val = 100, act_val = None) -> None:
    super().__init__()
    self.max_val = max_val
    self.act_val = act_val or self.max_val
    self.cur_val = self.act_val
    self.size = size or (400, 20)
    self.paddings = (4, 4, 4, 4)
    self.color = color or (100, 100, 100)
    w, h, = self.size
    t, r, b, l = self.paddings
    self.image = Surface((w + r + l, h + t + b), pygame.SRCALPHA, 32).convert_alpha()
    self.rect = self.image.get_rect()
    self.bar_speed = 150
    self.side = side
    self.render()


  def update(self) -> None:
    if self.act_val == self.cur_val: return
    self.render()

  @property
  def inner_size(self) -> tuple[int]:
    t, r, b, l = self.paddings
    return (self.rect.w - r - l, self.rect.h - t - b) 
  
  def render(self) -> None:
    self.image.fill((0, 0, 0, 0))
    t, r, b, l = self.paddings
    w, h = self.inner_size
    width = w * self.cur_val / self.max_val
    surface = Surface((width, h))
    surface.fill(self.color)
    rect = surface.get_rect()
    rect.top = t
    rect.left = w - width + l if self.side == RIGHT else l
    self.image.blit(surface, rect)
    self.cur_val = max(self.act_val, self.cur_val - self.bar_speed / FPS)
    pygame.draw.line(self.image, WHITESMOKE, (0, t), (self.rect.w, t))
    pygame.draw.line(self.image, WHITESMOKE, (0, self.rect.h - b), (self.rect.w, self.rect.h - b))
    pygame.draw.line(self.image, WHITESMOKE, (l, 0), (l, self.rect.h))
    pygame.draw.line(self.image, WHITESMOKE, (self.rect.w - r, 0), (self.rect.w - r, self.rect.h))
    for i in range(1, 4):
      pygame.draw.line(self.image, WHITESMOKE, (l + i * w / 4, 0), (l + i * w / 4, self.rect.h))



  