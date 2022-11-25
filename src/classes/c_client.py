import socket as sck
from socket import socket
from typing import Callable
from ..defaults import HOST, PORT
from threading import Thread
from .c_connactable import Connectable

class SocketClient(Connectable):
  def __init__(self, handler: Callable = None) -> None:
    super().__init__(handler)
    self.reset()
  
  def main(self) -> None:
    if self.is_up: return
    self.is_up = True
    self.error = None
    while True:
      if not self.is_up:
        break
      try:
        with socket(sck.AF_INET, sck.SOCK_STREAM) as s:
          self.socket = s
          s.connect((HOST, PORT))
          s.setblocking(0)
          self.connected = True
          while True:
            if not self.is_up:
              break
            
            try:
              data = s.recv(1024)
              if data and self.handler:
                self.handler(data.decode())
            except BlockingIOError:
              pass

            if len(self.data):
              request = self.data[0]
              s.sendall(request.encode())
              self.data = self.data[1:]

      except Exception as e:
        print('Client error: ', e, e.__class__.__name__)
        self.error = e
        return

  @property
  def connecting(self) -> bool:
    return self.is_up and not self.connected and not self.error