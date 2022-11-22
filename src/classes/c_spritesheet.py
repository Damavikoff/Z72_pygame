from time import time
import pygame
from pygame.rect import Rect
from pygame.image import load
from pygame.sprite import Sprite
from pygame.surface import Surface
from pygame.transform import scale
from .c_hitbox import Hitbox
from ..defaults import FPS

class SpriteSheet(Sprite):
  def __init__(self, path: str,
                     size: tuple[int],
                     hitbox_b: list[int] = None,
                     hitbox_a: list[int] = None,
                     scale = 1,
                     speed = 1,
                     is_looped = False,
                     is_left = True) -> None:
    super().__init__()
    h_a = hitbox_a if hitbox_a else []
    h_b = hitbox_b if hitbox_b else []
    self.spritesheet = load(path).convert_alpha()
    self.detected = False
    self.size = size
    self.scale = scale
    self.speed = speed
    self.is_left = is_left
    self.tick = 0
    self.index = 0
    self.is_completed = False
    self.is_looped = is_looped
    self.last_index = None
    self.frames = self.get_frames()
    self.image = Surface([v * self.scale for v in self.size], pygame.SRCALPHA, 32).convert_alpha()
    self.rect = self.image.get_rect()
    self.hitbox_body = self.get_hitbox(h_b)
    self.hitbox_weapon = self.get_hitbox(h_a)
    self.set_frame()

  def get_hitbox(self, hitboxes: list[tuple[int]]) -> list[Hitbox]:
    h_list = []
    x, y = self.rect.bottomright if self.is_left else self.rect.bottomleft
    for v in hitboxes:
      p_x = -v[2] if self.is_left else v[2]
      h_list.append(Hitbox((v[0], v[1]), (p_x * self.scale + x, -v[3] * self.scale + y), self.scale, self.is_left))
    return h_list

  def get_frames(self) -> list[Surface]:
    frames = []
    w, h = self.size
    for i in range(self.frame_count):
      image = Surface(self.size, pygame.SRCALPHA, 32).convert_alpha()
      # image = Surface(self.size)
      image.blit(self.spritesheet, (0, 0), (w * i, 0, w, h))
      frames.append(image)
    return frames

  def set_frame(self, index = 0) -> None:
    if self.last_index == index: return
    self.index = index
    self.image.fill((0, 0, 0, 0))
    self.image.blit(scale(self.frames[index], [v * self.scale for v in self.size]), (0, 0))
    self.last_index = index

  @property
  def frame_count(self) -> int:
    return int(self.spritesheet.get_width() / self.size[0])

  @property
  def hitbox_b(self) -> Hitbox:
    return self.hitbox_body[self.index] if len(self.hitbox_body) > self.index else None

  @property
  def hitbox_a(self) -> Hitbox:
    return self.hitbox_weapon[self.index] if len(self.hitbox_weapon) > self.index else None

  def update(self) -> None:
    if self.is_completed: return
    self.tick += self.speed / FPS
    index = int(self.tick % self.frame_count)
    if self.tick >= self.frame_count and not self.is_looped:
      self.is_completed = True
    elif index != self.index:
      self.set_frame(index)

  def reset(self) -> None:
    self.tick = 0
    self.index = 0
    self.set_frame(0)
    self.is_completed = False
    if self.hitbox_a:
      self.detected = False
  