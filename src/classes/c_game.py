import pygame
from pygame.sprite import Group
from pygame.surface import Surface
from .c_character import CharLord, CharWarrior
from .c_scene import Scene
from ..defaults import ACT_ATTACK, ACT_JUMP, ACT_RUN_LEFT, ACT_RUN_RIGHT, SCENE_IMAGES, DEF_WIN_W, LEFT, RIGHT

CONTROLS_1 = {
  pygame.K_a: ACT_RUN_LEFT,
  pygame.K_d: ACT_RUN_RIGHT,
  pygame.K_r: ACT_ATTACK,
  pygame.K_w: ACT_JUMP
}

CONTROLS_2 = {
  pygame.K_LEFT: ACT_RUN_LEFT,
  pygame.K_RIGHT: ACT_RUN_RIGHT,
  pygame.K_SPACE: ACT_ATTACK,
  pygame.K_UP: ACT_JUMP
}

class Game:
  def __init__(self, size: tuple[int]) -> None:
      super().__init__()
      self.characters = Group()
      self.scene = Scene(size, SCENE_IMAGES)
      self.char1 = CharWarrior(scale = 3.2, controls = CONTROLS_1, position = (100, size[1] - 54))
      self.char2 = CharLord(scale = 2.9, controls = CONTROLS_2, position = (DEF_WIN_W - 190, size[1] - 55))
      self.characters.add(self.char1, self.char2)
      self.surface = Surface(size)
      self.width = self.surface.get_width()

  def draw(self, target: Surface) -> None:
    # self.surface.fill((60, 60, 60))
    self.surface.blit(self.scene.image, (0, 0))
    self.characters.draw(self.surface)
    target.blit(self.surface, (0, 0))

  def update(self) -> None:
    self.update_movement()
    self.scene.update()
    self.characters.update()

  def update_movement(self) -> None:
    r1 = self.char1.fit_rect
    r2 = self.char2.fit_rect
    x1 = self.char1.position[0]
    dx1 = x1 + r1.w
    x2 = self.char2.position[0]
    dx2 = x2 + r2.w
    self.char1.movement[LEFT] = x1 > 0 and x1 < x2 or x1 > dx2
    self.char1.movement[RIGHT] = dx1 < self.width and dx1 > dx2 or dx1 < x2
    self.char2.movement[LEFT] = x2 > 0 and x2 < x1 or x2 > dx1
    self.char2.movement[RIGHT] = dx2 < self.width and dx2 > dx1 or dx2 < x1

  def handle_keydown(self, key) -> None:
    if key in CONTROLS_1:
      self.char1.handle_control(key)
    if key in CONTROLS_2:
      self.char2.handle_control(key)
  
  def handle_keyup(self, key) -> None:
    if key in CONTROLS_1:
      self.char1.handle_control(key, True)
    if key in CONTROLS_2:
      self.char2.handle_control(key, True)
