from pygame.rect import Rect
from pygame.surface import Surface

class Hitbox(Rect):
  def __init__(self, size: list[int], pos: tuple[int], scale = 1, is_left = True) -> None:
    super().__init__(0, 0, *[v * scale for v in size])
    self.detected = False
    if is_left:
      self.bottomright = pos
    else:
      self.bottomleft = pos