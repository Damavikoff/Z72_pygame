import socket as sck
from socket import socket
from ..defaults import HOST, PORT
from threading import Thread
from time import sleep

class SocketClient(Thread):
  def __init__(self) -> None:
    self.socket: socket | None = None
    self.is_running = False
    self.is_connected = False
    self.is_up = False
    self.data: list[str] = []
    super().__init__(target = self.start_t, daemon = True)

  def send(self, data: str) -> None:
    self.data.append(data)
  
  def start_t(self) -> None:
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
          self.is_connected = True
          while True:
            if not self.is_up:
              self.stop()
              break
            if len(self.data):
              request = self.data[0]
              print('Preparing request: ', request)
              s.sendall(request.encode())
              response = s.recv(1024)
              print('Server response: ', response.decode())
              self.data = self.data[1:]
      except Exception as e:
        print('Client error: ', e)
        self.error = e
      finally:
        self.stop()

  def stop(self) -> None:
    if self.socket: self.socket.close()
    self.socket = None
    self.is_connected = False
    self.is_up = False

  @property
  def connecting(self) -> bool:
    return self.is_up and not self.is_connected and not self.error

  @property
  def succesded(self) -> bool:
    return self.is_up and self.is_connected and not self.error

  @property
  def failed(self) -> bool:
    return self.error