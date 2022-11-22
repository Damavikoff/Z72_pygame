import pygame
from pygame.sprite import Group
from pygame.surface import Surface
from .c_character import CharLord, CharWarrior, Character
from .c_scene import Scene
from .c_text import Text
from ..defaults import ACT_ATTACK, ACT_JUMP, ACT_RUN_LEFT, ACT_RUN_RIGHT, ATTACK_1, ATTACK_2, SCENE_IMAGES, DEF_WIN_W, LEFT, RIGHT

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


MSG_GAME_OVER = """
        GAME OVER
Would you like to continue?

   YES              NO
 [ENTER]         [ESCAPE]
"""


class Game:
  def __init__(self, size: tuple[int]) -> None:
      super().__init__()
      self.characters = Group()
      self.ui = Group()
      self.scene = Scene(size, SCENE_IMAGES)
      self.char1 = CharWarrior(scale = 3.2, controls = CONTROLS_1, position = (100, size[1] - 54))
      self.char2 = CharLord(scale = 2.9, controls = CONTROLS_2, position = (size[0] - 190, size[1] - 55))
      self.ui.add(self.char1.health_bar, self.char2.health_bar)
      self.char1.health_bar.rect.topleft = (20, 20)
      self.char2.health_bar.rect.topright = (size[0] - 20, 20)
      self.characters.add(self.char1, self.char2)
      self.surface = Surface(size)
      self.width = self.surface.get_width()
      self.caption: Text | None = None
      self.is_paused = False
      self.is_network = False
      self.can_proceed = True
      self.is_host = False
      self.remote_client = None

  def draw(self, target: Surface) -> None:
    self.surface.fill((60, 60, 60))
    self.surface.blit(self.scene.image, (0, 0))
    self.characters.draw(self.surface)
    self.ui.draw(self.surface)
    if self.caption:
      rect = self.caption.get_rect()
      rect.center = self.surface.get_rect().center
      self.surface.blit(self.caption, rect)
    target.blit(self.surface, (0, 0))

  def update(self) -> None:
    self.set_movement()
    self.scene.update()
    self.characters.update()
    self.check_hit()
    if self.is_someone_dead and not self.caption:
      self.set_caption(MSG_GAME_OVER)
      self.can_proceed = False

  def set_movement(self) -> None:
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

  def check_hit(self) -> None:
    chars:list[Character] = [*self.characters.sprites()]
    for c in chars:
      if c.is_attacking:
        c.check_hit([v for v in chars if v != c])

  def set_caption(self, text: str, size: int = 28, alignment = 0) -> None:
    color = (200, 144, 25)
    self.caption = Text(text = text, size = size, color = color, alignment = alignment, paddings = (20, 0, 20, 0))
    w, h = self.caption.get_size()
    pygame.draw.line(self.caption, color, (0, 1), (w, 1))
    pygame.draw.line(self.caption, color, (0, h - 1), (w, h - 1))

  def handle_keydown(self, key) -> None:
    if not self.can_proceed: return
    if key in CONTROLS_1:
      self.char1.handle_control(key)
    if key in CONTROLS_2:
      self.char2.handle_control(key)
  
  def handle_keyup(self, key) -> None:
    if not self.can_proceed: return
    if key in CONTROLS_1:
      self.char1.handle_control(key, True)
    if key in CONTROLS_2:
      self.char2.handle_control(key, True)

  @property
  def is_someone_dead(self) -> bool:
    chars: list[Character] = self.characters.sprites()
    return next((v for v in chars if not v.is_alive), False)
