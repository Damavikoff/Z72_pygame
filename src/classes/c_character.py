from time import time
import pygame
from math import sqrt
from pygame.sprite import Sprite
from pygame.rect import Rect
from pygame.surface import Surface
from .c_spritesheet import SpriteSheet
from .c_hitbox import Hitbox
from .c_healthbar import HealthBar
from ..defaults import WARRIOR_1, WARRIOR_2, FPS
from ..defaults import ATTACK_1, ATTACK_2, ATTACK_3, DEATH, FALL, GET_HIT, IDLE, JUMP, RUN, ACT_ATTACK, ACT_JUMP, ACT_RUN_LEFT, ACT_RUN_RIGHT, LEFT, RIGHT

class Character(Sprite):

  def __init__(self, sprites: dict = None, scale = 1, controls: dict = None, position: tuple[float] = None) -> None:
    super().__init__()
    self.size = (0, 0)
    self.sprites = sprites if sprites else {}
    self.action_list = []
    self.action_queue = []
    self.health = 500
    self.damage = 20
    self.action = IDLE
    self.side = RIGHT
    self.scale = scale
    self.fit_box = [0, 0, 48, 0]
    self.init_pos = (0, 0) if not position else position
    self.position = [*self.init_pos]
    self.ground = 0
    self.show_hitboxes = False
    self.controls = {} if controls is None else controls
    self.move_speed = 390
    self.jump_speed = 0
    self.health_bar: HealthBar | None = None
    self.sprites = {}
    self.movement = {
      LEFT: True,
      RIGHT: True
    }

  @property
  def is_alive(self) -> bool:
    return self.health_bar.act_val > 0

  @property
  def active_sprite(self) -> SpriteSheet:
    return self.sprites[self.action or IDLE]

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
  def is_jumping(self) -> bool:
    return self.action in [JUMP, FALL]

  @property
  def is_moving(self) -> bool:
    return not set(self.action_list).isdisjoint([ACT_RUN_LEFT, ACT_RUN_RIGHT])

  @property
  def is_busy(self) -> None:
    return self.is_attacking or self.is_jumping

  @property
  def scaled_size(self) -> list[int]:
    return [v * self.scale for v in self.size]

  @property
  def sprite_ground(self) -> float:
    return (self.size[1] - self.fit_box[2]) * self.scale

  @property
  def hitboxes(self) -> tuple[Hitbox]:
    h_b = self.get_real_hitbox(self.active_sprite.hitbox_b)
    h_a = self.get_real_hitbox(self.active_sprite.hitbox_a) if self.active_sprite.hitbox_a else None
    return (h_a, h_b)

  def get_real_hitbox(self, hitbox: Hitbox) -> Rect:
    h_x = hitbox.copy()
    if (self.side == RIGHT):
      h_x.left = self.rect.left + h_x.left
    else:
      h_x.left = self.rect.right - h_x.right
    h_x.top = self.rect.top + h_x.top
    return h_x

  def set_static(self, action, frame) -> None:
    self.action = action
    self.active_sprite.last_index = -1
    self.active_sprite.set_frame(frame)
    self.set_pos()

  def set_new_action(self) -> None:
    if len(self.action_queue):
      self.set_action_sprite(self.action_queue[0])
      self.action_queue = [v for v in self.action_queue if v != self.action]
    else:
      self.set_action_sprite(RUN if self.is_moving and self.movement[self.side] else IDLE)

  def update_action(self) -> None:
    if self.is_moving and not self.is_busy:
      self.move_x()
    if self.is_jumping:
      self.move_y()
    self.active_sprite.update()

  def update(self) -> None:
    # self.set_static(ATTACK_3, 7)
    # self.render_hitboxes()
    # return
    self.health_bar.update()
    if not self.is_alive and self.active_sprite.is_completed: return
    if not self.action:
      self.set_action_sprite(RUN if self.is_moving and self.movement[self.side] else IDLE)
    elif self.action == RUN and not self.movement[self.side]:
      self.set_action_sprite(IDLE)
    if self.active_sprite.is_completed:
      self.set_new_action()
    else:
      self.update_action()
    if self.show_hitboxes:
      self.render_hitboxes()
    
    self.set_pos()

  def render_hitboxes(self) -> None:
    pygame.draw.line(self.active_sprite.image, (255, 0, 255), (0, self.sprite_ground), (self.size[0] * self.scale, self.sprite_ground))
    if self.active_sprite.hitbox_b:
      pygame.draw.rect(self.active_sprite.image, (255, 255, 0), self.active_sprite.hitbox_b, 1)
    if self.active_sprite.hitbox_a:
      pygame.draw.rect(self.active_sprite.image, (255, 0, 0), self.active_sprite.hitbox_a, 1)
    pygame.draw.rect(self.active_sprite.image, (0, 255, 255), self.fit_rect, 1)

  def move_x(self) -> None:
    if not self.movement[self.side]: return
    speed = self.move_speed / 3 if self.is_jumping else self.move_speed
    self.position[0] += int(speed * (1 if self.side == RIGHT else -1) / FPS)

  def set_action_sprite(self, action) -> None:
    self.action = action
    self.active_sprite.reset()

  def move_y(self) -> None:
    if self.is_moving:
      self.move_x()
    sign = (-1, 1)[int(self.action == JUMP)]
    self.ground += sign * (self.jump_speed / FPS - sign * 19.8 / (FPS**2 * 2)) * 95
    self.jump_speed += -sign * 9.8 / FPS
    if self.action == JUMP and self.jump_speed <= 0:
      self.jump_speed = 0
      self.set_action_sprite(FALL)
    elif self.action == FALL and self.ground <= 0:
      self.ground = 0
      self.action = None

  def set_pos(self) -> None:
    if not self.active_sprite: return
    x, y = self.position
    self.active_sprite.rect.bottom = self.init_pos[1] + self.fit_box[2] * self.scale - self.ground
    self.active_sprite.rect.left = x - self.fit_rect.left

  def set_fit_rect(self) -> Rect:
    fit_scaled = [v * self.scale for v in self.fit_box]
    p_t, p_r, p_b, p_l = fit_scaled
    w, h = self.scaled_size
    rect = Rect(0, 0, w - p_r - p_l, h - p_t - p_b)
    rect.center = self.rect.center
    rect.top = p_t
    self.fit_rect = rect

  def set_action_queue(self, action) -> None:
    if isinstance(action, list):
      self.action_queue = [*self.action_queue, *action]
    else:
      self.action_queue.append(action)

  def attack(self) -> None:
    if self.is_jumping: return
    if ATTACK_3 in [*self.action_queue, self.action]: return
    if ATTACK_2 in self.action_queue:
      self.set_action_queue(ATTACK_3)
    elif self.action == ATTACK_1:
      self.set_action_queue(ATTACK_2)
    else:
      self.set_action_sprite(ATTACK_1)

  def run(self, dir) -> None:
    self.side = dir
    if self.is_busy or not self.movement[self.side] or self.action == RUN: return
    self.set_action_sprite(RUN)

  def jump(self) -> None:
    if self.is_jumping: return
    self.jump_speed = 5
    self.set_action_sprite(JUMP)

  def handle_control(self, control, disable = False) -> None:
    if not self.is_alive: return
    if control not in self.controls: return
    action = self.controls[control]
    if disable:
      self.action_list = [ v for v in self.action_list if v != action ]
      if action in [ACT_RUN_LEFT, ACT_RUN_RIGHT] and not self.is_moving and self.action == RUN:
        self.set_action_sprite(IDLE)
      return
    if action not in self.action_list: self.action_list.append(action)
    if action == ACT_ATTACK:
      self.attack()
    elif action in [ACT_RUN_LEFT, ACT_RUN_RIGHT]:
      self.run(LEFT if action == ACT_RUN_LEFT else RIGHT)
    elif action == ACT_JUMP:
      self.jump()

  def check_hit(self, chars: list['Character']) -> None:
    if not self.is_attacking or not self.active_sprite.hitbox_a: return
    h_a = self.hitboxes[0]
    for c in chars:
      if not c.is_alive: return
      h_b = c.hitboxes[1]
      if (h_a.colliderect(h_b) and not self.active_sprite.detected) and c.is_alive:
        c.health_bar.remove_points(self.damage)
        self.active_sprite.detected = True
        if not c.is_alive:
          c.set_action_sprite(DEATH)

  def reset(self) -> None:
    self.position = [*self.init_pos]
    self.jump_speed = 0
    self.ground = 0
    self.action_queue = []
    self.action = None
    self.health_bar.reset()

#######################################################################################

class CharWarrior(Character):
  def __init__(self, scale = 1, controls: dict = None, position: tuple[float] = None) -> None:
    super().__init__(None, scale, controls, position)
    self.size = (135, 135)
    self.damage = 20
    self.sprites = {
      ATTACK_1: SpriteSheet(WARRIOR_1[ATTACK_1][0], self.size, WARRIOR_1[ATTACK_1][1], WARRIOR_1[ATTACK_1][2], scale, 10),
      ATTACK_2: SpriteSheet(WARRIOR_1[ATTACK_2][0], self.size, WARRIOR_1[ATTACK_2][1], WARRIOR_1[ATTACK_2][2], scale, 10),
      ATTACK_3: SpriteSheet(WARRIOR_1[ATTACK_3][0], self.size, WARRIOR_1[ATTACK_3][1], WARRIOR_1[ATTACK_3][2], scale, 10),
      DEATH: SpriteSheet(WARRIOR_1[DEATH][0], self.size, WARRIOR_1[DEATH][1], None, scale, 9),
      FALL: SpriteSheet(WARRIOR_1[FALL][0], self.size, WARRIOR_1[FALL][1], None, scale, 11, True),
      GET_HIT: SpriteSheet(WARRIOR_1[GET_HIT][0], self.size, WARRIOR_1[GET_HIT][1], None, scale, 11),
      IDLE: SpriteSheet(WARRIOR_1[IDLE][0], self.size, WARRIOR_1[IDLE][1], None, scale, 11, True),
      JUMP: SpriteSheet(WARRIOR_1[JUMP][0], self.size, WARRIOR_1[JUMP][1], None, scale, 11, True),
      RUN: SpriteSheet(WARRIOR_1[RUN][0], self.size, WARRIOR_1[RUN][1], None, scale, 11, True)
    }
    self.health_bar = HealthBar(color = (204, 44, 55), max_val = self.health)
    self.fit_box = [0, 52, 48, 55]
    self.set_fit_rect()


class CharLord(Character):
  def __init__(self, scale = 1, controls: dict = None, position: tuple[float] = None) -> None:
    super().__init__(None, scale, controls, position)
    self.size = (162, 162)
    self.damage = 35
    self.sprites = {
      ATTACK_1: SpriteSheet(WARRIOR_2[ATTACK_1][0], self.size, WARRIOR_2[ATTACK_1][1], WARRIOR_2[ATTACK_1][2], scale, 10),
      ATTACK_2: SpriteSheet(WARRIOR_2[ATTACK_2][0], self.size, WARRIOR_2[ATTACK_2][1], WARRIOR_2[ATTACK_2][2], scale, 10),
      ATTACK_3: SpriteSheet(WARRIOR_2[ATTACK_3][0], self.size, WARRIOR_2[ATTACK_3][1], WARRIOR_2[ATTACK_3][2], scale, 10),
      DEATH: SpriteSheet(WARRIOR_2[DEATH][0], self.size, WARRIOR_2[DEATH][1], None, scale, 9),
      FALL: SpriteSheet(WARRIOR_2[FALL][0], self.size, WARRIOR_2[FALL][1], None, scale, 11, True),
      GET_HIT: SpriteSheet(WARRIOR_2[GET_HIT][0], self.size, WARRIOR_2[GET_HIT][1], None, scale, 11),
      IDLE: SpriteSheet(WARRIOR_2[IDLE][0], self.size, WARRIOR_2[IDLE][1], None, scale, 11, True),
      JUMP: SpriteSheet(WARRIOR_2[JUMP][0], self.size, WARRIOR_2[JUMP][1], None, scale, 11, True),
      RUN: SpriteSheet(WARRIOR_2[RUN][0], self.size, WARRIOR_2[RUN][1], None, scale, 11, True)
    }
    self.side = LEFT
    self.health_bar = HealthBar(color = (77, 164, 126), max_val = self.health, side = RIGHT)
    self.fit_box = [0, 68, 62, 68]
    self.set_fit_rect()
  
