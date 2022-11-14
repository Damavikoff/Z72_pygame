import pygame
from pygame.sprite import Group
from pygame.surface import Surface
from .c_character import Character, CharWarrior
from .c_scene import Scene
from ..defaults import ACT_ATTACK, ACT_JUMP, ACT_RUN_LEFT, ACT_RUN_RIGHT, SCENE_IMAGES

CONTROLS_1 = {
  pygame.K_a: ACT_RUN_LEFT,
  pygame.K_d: ACT_RUN_RIGHT,
  pygame.K_r: ACT_ATTACK,
  pygame.K_w: ACT_JUMP
}

class Game:
  def __init__(self, size: tuple[int]) -> None:
      super().__init__()
      ground = size[1] - 52
      self.characters = Group()
      self.scene = Scene(size, SCENE_IMAGES)
      self.char1 = CharWarrior(scale = 3, controls = CONTROLS_1, position = (100, ground))
      self.characters.add(self.char1)
      self.surface = Surface(size)

  def draw(self, target: Surface) -> None:
    # self.surface.fill((60, 60, 60))
    self.surface.blit(self.scene.image, (0, 0))
    self.characters.draw(self.surface)
    target.blit(self.surface, (0, 0))

  def update(self) -> None:
    self.scene.update()
    self.characters.update()

  def handle_keydown(self, key) -> None:
    if key in CONTROLS_1:
      self.char1.handle_control(key)
  
  def handle_keyup(self, key) -> None:
    if key in CONTROLS_1:
      self.char1.handle_control(key, True)
