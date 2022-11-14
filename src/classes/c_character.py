import pygame
from pygame.sprite import Sprite
from pygame.rect import Rect
from pygame.surface import Surface
from .c_spritesheet import SpriteSheet
from .c_hitbox import Hitbox
from ..defaults import WARRIOR_1, WARRIOR_2, FPS
from ..defaults import ATTACK_1, ATTACK_2, ATTACK_3, DEATH, FALL, GET_HIT, IDLE, JUMP, RUN, ACT_ATTACK, ACT_JUMP, ACT_RUN_LEFT, ACT_RUN_RIGHT, LEFT, RIGHT

class Character(Sprite):

  def __init__(self, sprites: dict = None, scale = 1, controls: dict = None, position: tuple[float] = None) -> None:
    super().__init__()
    self.sprites = sprites if sprites else {}
    self.action_queue = []
    self.action = IDLE
    self.side = RIGHT
    self.scale = scale
    self.fit_box = [0, 0, 48, 0]
    self.init_pos = (0, 0) if not position else position
    self.position = [v for v in self.init_pos]
    self.show_hitboxes = False
    self.controls = {} if controls is None else controls
    self.speed = 390
    self.sprites = {}
    self.movement = {
      LEFT: True,
      RIGHT: True
    }
    # self.active_sprite = self.sprites[0]
    # self.image = self.active_sprite.image
    # self.rect = self.image.get_rect()
    

  @property
  def active_sprite(self) -> SpriteSheet:
    return self.sprites[self.action]

  @property
  def image(self) -> Surface:
    image = self.active_sprite.image
    if self.side == LEFT:
      return pygame.transform.flip(image, True, False)
    return image

  @property
  def rect(self) -> Rect:
    return self.active_sprite.rect

  @property
  def is_attacking(self) -> bool:
    return not set([*self.action_queue, self.action]).isdisjoint([ATTACK_1, ATTACK_2, ATTACK_3])

  @property
  def scaled_size(self) -> list[int]:
    return [v * self.scale for v in self.size]

  @property
  def sprite_ground(self) -> float:
    return (self.size[1] - self.fit_box[2]) * self.scale


  def update(self) -> None:
    if not self.action or (self.action == RUN and not self.movement[self.side]): self.action = IDLE
    if self.action == RUN:
      self.move()
    self.set_pos()
    self.active_sprite.update()
    if self.show_hitboxes:
      self.render_hitboxes()
    if not self.active_sprite.is_completed: return
    self.active_sprite.reset()
    if len(self.action_queue):
      self.action = self.action_queue[0]
      self.action_queue = [v for v in self.action_queue if v != self.action]
    else:
      self.action = IDLE
    self.active_sprite.reset()
    self.set_pos()

  def render_hitboxes(self) -> None:
    pygame.draw.line(self.active_sprite.image, (255, 0, 255), (0, self.sprite_ground), (self.size[0] * self.scale, self.sprite_ground))
    if self.active_sprite.hitbox_b:
      pygame.draw.rect(self.active_sprite.image, (255, 255, 0), self.active_sprite.hitbox_b, 1)
    pygame.draw.rect(self.active_sprite.image, (0, 255, 255), self.fit_rect, 1)

  def move(self) -> None:
    if not self.movement[self.side]: return
    pos = self.position[0]
    self.position[0] = pos + int(self.speed * (1 if self.side == RIGHT else -1) / FPS)

  def set_pos(self) -> None:
    if not self.active_sprite: return
    x, y = self.position
    self.active_sprite.rect.bottom = self.init_pos[1] + self.fit_box[2] * self.scale
    self.active_sprite.rect.left = x - self.fit_rect.left

  def set_fit_rect(self) -> Rect:
    fit_scaled = [v * self.scale for v in self.fit_box]
    p_t, p_r, p_b, p_l = fit_scaled
    w, h = self.scaled_size
    rect = Rect(0, 0, w - p_r - p_l, h - p_t - p_b)
    rect.center = self.rect.center
    rect.top = p_t
    self.fit_rect = rect

  def set_action(self, action) -> None:
    if isinstance(action, list):
      self.action_queue = [*self.action_queue, *action]
    else:
      self.action_queue.append(action)

  def attack(self) -> None:
    if ATTACK_3 in [*self.action_queue, self.action]: return
    if ATTACK_2 in self.action_queue:
      self.set_action(ATTACK_3)
    elif self.action == ATTACK_1:
      self.set_action(ATTACK_2)
    else:
      self.action = ATTACK_1

  def run(self, dir) -> None:
    self.side = dir
    if self.is_attacking or not self.movement[self.side]: return
    self.action = RUN
    self.active_sprite.reset()

  def handle_control(self, control, disable = False) -> None:
    if control not in self.controls: return
    action = self.controls[control]
    if disable:
      if action in [ACT_RUN_LEFT, ACT_RUN_RIGHT]:
        self.action = IDLE
      return
    if action == ACT_ATTACK:
      self.attack()
    elif action in [ACT_RUN_LEFT, ACT_RUN_RIGHT]:
      self.run(LEFT if action == ACT_RUN_LEFT else RIGHT)

#######################################################################################

class CharWarrior(Character):
  def __init__(self, scale = 1, controls: dict = None, position: tuple[float] = None) -> None:
    super().__init__(None, scale, controls, position)
    self.size = (135, 135)
    self.sprites = {
      ATTACK_1: SpriteSheet(WARRIOR_1[ATTACK_1][0], self.size, WARRIOR_1[ATTACK_1][1], scale, 10),
      ATTACK_2: SpriteSheet(WARRIOR_1[ATTACK_2][0], self.size, WARRIOR_1[ATTACK_2][1], scale, 10),
      ATTACK_3: SpriteSheet(WARRIOR_1[ATTACK_3][0], self.size, WARRIOR_1[ATTACK_3][1], scale, 10),
      DEATH: SpriteSheet(WARRIOR_1[DEATH][0], self.size, WARRIOR_1[DEATH][1], scale, 11),
      FALL: SpriteSheet(WARRIOR_1[FALL][0], self.size, WARRIOR_1[FALL][1], scale, 11),
      GET_HIT: SpriteSheet(WARRIOR_1[GET_HIT][0], self.size, WARRIOR_1[GET_HIT][1], scale, 11),
      IDLE: SpriteSheet(WARRIOR_1[IDLE][0], self.size, WARRIOR_1[IDLE][1], scale, 11),
      JUMP: SpriteSheet(WARRIOR_1[JUMP][0], self.size, WARRIOR_1[JUMP][1], scale, 11),
      RUN: SpriteSheet(WARRIOR_1[RUN][0], self.size, WARRIOR_1[RUN][1], scale, 11)
    }
    self.sprites[RUN].is_looped = True
    self.fit_box = [0, 52, 48, 55]
    self.set_fit_rect()


class CharLord(Character):
  def __init__(self, scale = 1, controls: dict = None, position: tuple[float] = None) -> None:
    super().__init__(None, scale, controls, position)
    self.size = (162, 162)
    self.sprites = {
      ATTACK_1: SpriteSheet(WARRIOR_2[ATTACK_1][0], self.size, WARRIOR_2[ATTACK_1][1], scale, 10),
      ATTACK_2: SpriteSheet(WARRIOR_2[ATTACK_2][0], self.size, WARRIOR_2[ATTACK_2][1], scale, 10),
      ATTACK_3: SpriteSheet(WARRIOR_2[ATTACK_3][0], self.size, WARRIOR_2[ATTACK_3][1], scale, 10),
      DEATH: SpriteSheet(WARRIOR_2[DEATH][0], self.size, WARRIOR_2[DEATH][1], scale, 11),
      FALL: SpriteSheet(WARRIOR_2[FALL][0], self.size, WARRIOR_2[FALL][1], scale, 11),
      GET_HIT: SpriteSheet(WARRIOR_2[GET_HIT][0], self.size, WARRIOR_2[GET_HIT][1], scale, 11),
      IDLE: SpriteSheet(WARRIOR_2[IDLE][0], self.size, WARRIOR_2[IDLE][1], scale, 11),
      JUMP: SpriteSheet(WARRIOR_2[JUMP][0], self.size, WARRIOR_2[JUMP][1], scale, 11),
      RUN: SpriteSheet(WARRIOR_2[RUN][0], self.size, WARRIOR_2[RUN][1], scale, 11)
    }
    self.side = LEFT
    self.sprites[RUN].is_looped = True
    self.fit_box = [0, 68, 62, 68]
    self.set_fit_rect()
  
