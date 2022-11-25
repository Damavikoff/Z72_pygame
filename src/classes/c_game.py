from time import sleep
from tkinter import OFF
import pygame
import sys
from pygame.sprite import Group
from pygame.surface import Surface
from .c_character import CharLord, CharWarrior, Character
from .c_scene import Scene
from .c_text import Text
from .c_caption import Caption
from .c_server import SocketServer
from .c_client import SocketClient
from ..defaults import ACT_ATTACK, ACT_JUMP, ACT_RUN_LEFT, ACT_RUN_RIGHT, ATTACK_1, ATTACK_2, M_CONNECTING, SCENE_IMAGES, DEF_WIN_W, LEFT, RIGHT
from ..defaults import M_LIST, M_MODE, M_GAME_OVER, M_CONNECTION_ERROR, M_CLENT_AWAIT, M_CONNECTION_FAILED
from ..defaults import CLIENT, SERVER, OFFLINE, ONLINE, CONNECTING, CLIENT_AWAIT
from ..defaults import ALIGN_LEFT, ALIGN_CENTER

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

SHOW_HITBOXES = pygame.K_q

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
      self.client = SocketClient(handler = self.handle_remote)
      self.server = SocketServer(handler = self.handle_remote)
      self.menu = self.get_menu()
      self.caption = None
      self.is_paused = True
      self.mode = OFFLINE
      self.side = None
      self.is_network = False
      self.set_caption(M_MODE)

  def handle_remote(self, action: str) -> None:
    if not self.remote_character or self.is_paused: return
    action_array = action.split(':')
    k, a = (int(action_array[0]), int(action_array[1]))
    self.remote_character.handle_control(a, k)

  def draw(self, target: Surface) -> None:
    self.surface.fill((60, 60, 60))
    self.surface.blit(self.scene.image, (0, 0))
    self.characters.draw(self.surface)
    self.ui.draw(self.surface)
    if self.caption:
      self.caption.draw(self.surface)
    target.blit(self.surface, (0, 0))

  def update(self) -> None:
    self.set_movement()
    self.scene.update()
    self.characters.update()
    self.check_hit()
    if self.is_someone_dead and not self.caption:
      self.set_caption(M_GAME_OVER)
    self.check_connection()


  def check_connection(self) -> None:
    if self.mode == CONNECTING and not self.client.connecting:
      if self.client.failed:
        self.client.reset()
        self.server.start()
        self.side = SERVER
        self.mode = CLIENT_AWAIT
        self.set_caption(M_CLENT_AWAIT)
      else:
        self.side = CLIENT
        self.caption = None
        self.mode = ONLINE
        self.is_paused = False
    elif self.mode == CLIENT_AWAIT and self.server.connected:
      self.caption = None
      self.mode = ONLINE
      self.is_paused = False
    elif self.mode == ONLINE:
      if self.side == SERVER and self.server.failed or self.side == CLIENT and self.client.failed:
        self.set_caption(M_CONNECTION_ERROR)
        self.mode = None

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

  def set_caption(self, caption) -> None:
    if caption in self.menu:
      self.caption = self.menu[caption]
      self.is_paused = True
  
  def handle_control(self, key, is_keyup = False) -> None:
    if self.caption and not is_keyup:
      return self.caption.run(key)
    if key == SHOW_HITBOXES and not is_keyup:
      self.char1.show_hitboxes = not self.char1.show_hitboxes
      self.char2.show_hitboxes = not self.char2.show_hitboxes
      return

    if self.is_paused: return
    if key in CONTROLS_1 and (self.mode == OFFLINE or self.host_character == self.char1):
      self.char1.handle_control(key, is_keyup)
    if key in CONTROLS_2 and (self.mode == OFFLINE or self.host_character == self.char2):
      self.char2.handle_control(key, is_keyup)

    if self.mode != ONLINE: return
    action = f"{int(is_keyup)}:{key}"
    if self.side == CLIENT and self.client.succeeded:
      self.client.send(action)
    elif self.side == SERVER and self.server.succeeded:
      self.server.send(action)

  def set_mode(self, mode = OFFLINE):
    self.caption = None
    self.mode = mode
    if mode == OFFLINE:
      self.mode = mode
      if self.is_someone_dead:
        self.reset()
      self.is_paused = False
    elif mode == CONNECTING:
      self.side = None
      self.server.reset()
      self.client.reset()
      self.client.start()
      self.set_caption(M_CONNECTING)

  def reset(self) -> None:
    self.is_paused = True
    chars: list[Character] = self.characters.sprites()
    for c in chars:
      c.reset()
    self.client.reset()
    self.server.reset()
    self.caption = None
    self.is_paused = False

  def reset_server(self) -> None:
    self.server.reset()
    self.mode = None
    self.set_caption(M_MODE)


  def exit(self):
    # pygame.display.quit()
    pygame.quit()
    sys.exit()

  @property
  def is_someone_dead(self) -> bool:
    chars: list[Character] = self.characters.sprites()
    return next((v for v in chars if not v.is_alive), False)

  @property
  def remote_character(self) -> Character | None:
    if self.mode == OFFLINE: return None
    return self.char1 if self.side == CLIENT else self.char2

  @property
  def host_character(self) -> Character | None:
    if self.mode == OFFLINE: return None
    return self.char1 if self.side == SERVER else self.char2

  def get_menu(self) -> dict[int, Caption]:
    center = self.surface.get_rect().center
    return {
      M_MODE: Caption(text = M_LIST[M_MODE], center = center, actions = {
        pygame.K_1: [self.set_mode, [OFFLINE]],
        pygame.K_2: [self.set_mode, [CONNECTING]],
        pygame.K_3: [self.exit, []]
      }),
      M_GAME_OVER: Caption(text = M_LIST[M_GAME_OVER], center = center, actions = {
        pygame.K_ESCAPE: [self.set_caption, [M_MODE]],
        pygame.K_RETURN: [self.reset, []]
      }),
      M_CONNECTING: Caption(text = M_LIST[M_CONNECTING], align = ALIGN_CENTER , center = center),
      M_CLENT_AWAIT: Caption(text = M_LIST[M_CLENT_AWAIT], align = ALIGN_CENTER , center = center, actions = {
        pygame.K_ESCAPE: [self.reset_server, []]
      }),
      M_CONNECTION_ERROR: Caption(text = M_LIST[M_CONNECTION_ERROR], center = center, actions = {
        pygame.K_RETURN: [self.set_mode, [OFFLINE]],
        pygame.K_ESCAPE: [self.set_caption, [M_MODE]]
      })
    }

  
