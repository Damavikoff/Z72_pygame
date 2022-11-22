from cgitb import text
import pygame.freetype
from pygame.surface import Surface
import pygame.font

DEF_FONT = pygame.font.get_default_font()

class Text(Surface):
  def __init__(self, text = 'text', size: int = 14, width: int = None, color: tuple[int] = None, paddings: tuple[int] = None, alignment: int = 0) -> None:
    self.text = text
    self.size = size
    self.width = width
    self.color = color or (0, 0, 0)
    self.font = pygame.font.SysFont('monospace', self.size, True)# pygame.font.Font(DEF_FONT, self.size)
    self.paddings = paddings or (0, 0, 0, 0)
    self.alignment = alignment
    surface = self.get_surface()
    super().__init__(surface.get_size(), pygame.SRCALPHA, 32)
    self.fill((0, 0, 0, 0))
    self.blit(surface, (0, 0))


  def get_bondless_surf(self) -> Surface:
    text_lines = self.text.splitlines()
    surfaces = []
    for t_line in text_lines:
      if not self.width:
        surfaces.append(self.font.render(t_line, True, self.color))
    return surfaces

  def get_surface(self) -> Surface:
    surfaces:list[Surface] = self.get_bondless_surf()
    t, r, b, l = self.paddings
    max_w = max(surfaces, key = lambda x: x.get_width()).get_width()
    w = max_w + r + l
    h = t + b + sum([v.get_height() for v in surfaces])
    surf = Surface((w, h), pygame.SRCALPHA, 32).convert_alpha()
    h_i = 0
    for i, v in enumerate(surfaces):
      rect = v.get_rect()
      if self.alignment == 0:
        rect.left = 0
      elif self.alignment == 1:
        rect.center = surf.get_rect().center
      else:
        rect.right = surf.get_rect().right
      rect.top = h_i + t
      h_i += rect.h
      surf.blit(v, rect)
    return surf