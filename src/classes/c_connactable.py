from threading import Thread
from typing import Callable
from socket import socket

class Connectable:
  def __init__(self, handler: Callable = None) -> None:
    self.is_up = False
    self.data: list[str] = []
    self.error = None
    self.socket: socket | None = None
    self.connected = False
    self.handler: Callable | None = handler
    self.thread: Thread | None = None

  def send(self, data: str) -> None:
    self.data.append(data)

  def stop(self) -> None:
    self.is_up = False

  def main(self) -> None:
    pass

  def start(self) -> None:
    if self.thread and not self.thread.is_alive():
      self.reset()
      self.thread.start()

  def reset(self) -> None:
    self.thread = None
    self.thread = Thread(target = self.main, daemon = True)
    if self.socket: self.socket.close()
    self.socket = None
    self.error = None
    self.is_up = False
    self.data = []
    self.connected = False

  
  @property
  def failed(self) -> bool:
    return self.error is not None

  @property
  def succeeded(self) -> bool:
    return self.connected and not self.failed