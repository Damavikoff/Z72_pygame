import pygame
from pygame import Surface
from pygame.locals import QUIT, KEYDOWN, KEYUP, MOUSEMOTION, MOUSEBUTTONDOWN, MOUSEBUTTONUP
from src.defaults import FPS, DEF_WIN_H, DEF_WIN_W, DEF_WIN_SCALE, DIR_ASSETS
from src.classes.c_game import Game
import os

DEF_WIN_W = 960
DEF_WIN_H = 600

def get_files(d: str) -> list[str]:
  return [f'{d}/{f}' for f in os.listdir(d) if os.path.isfile(os.path.join(d, f))]

class Application:
  def __init__(self) -> None:
    pygame.init()
    pygame.font.init()
    self.clock = pygame.time.Clock()
    # self.screen = self.set_window_size(DEF_WIN_SCALE)
    self.screen = pygame.display.set_mode((DEF_WIN_W, DEF_WIN_H))
    self.game = Game(self.screen.get_size())

  def set_window_size(self, scale: float) -> Surface:
    [width, height] = [ i * scale for i in self.display_size ]
    return pygame.display.set_mode((width, height))

  def init_app(self) -> None:
    pygame.display.set_caption('unknown')

  def handle_keydown(self, key: int) -> None:
    self.game.handle_keydown(key)
  
  def handle_keyup(self, key: int) -> None:
    self.game.handle_keyup(key)

  def start(self) -> None:
    self.init_app()
    while True:
      self.clock.tick(FPS)
      for event in pygame.event.get():
          if event.type == QUIT:
              return
          if event.type == KEYDOWN:
            self.handle_keydown(event.key)
          if event.type == KEYUP:
            self.handle_keyup(event.key)

      self.game.update()
      self.game.draw(self.screen)
      pygame.display.flip()

  @property
  def display_size(self) -> tuple[int]:
    displays = pygame.display.get_desktop_sizes()
    if (len(displays) == 0):
      return (200, 200)
    return displays[0]

def main():
  Application().start()

if __name__ == '__main__': main()
