import socket as sck
from socket import socket
from typing import Callable
from ..defaults import HOST, PORT
from threading import Thread
from .c_connactable import Connectable

class SocketServer(Connectable):
  def __init__(self, handler: Callable = None) -> None:
      super().__init__(handler)
      self.reset()

  def main(self) -> None:
    if self.is_up: return
    try:
      with socket(sck.AF_INET, sck.SOCK_STREAM) as s:
        s.setsockopt(sck.SOL_SOCKET, sck.SO_REUSEADDR, 1)
        s.bind((HOST, PORT))
        s.listen(1)
        self.socket = s
        conn, addr = s.accept()
        conn.setblocking(0)
        self.socket = s
        self.is_up = True
        with conn:
          self.connected = True
          print('Connection established: ', addr)
          while True:
            if not self.is_up:
              break

            try:
              data = conn.recv(1024)
              if data and self.handler:
                self.handler(data.decode())
            except BlockingIOError:
              pass

            if len(self.data):
              response = self.data[0]
              self.data = self.data[1:]
              conn.sendall(response.encode())
    except Exception as e:
      print('Server error: ', e, e.__class__.__name__)
      self.error = e
      return      

  def reset(self) -> None:
    # self.socket.shutdown(sck.SHUT_RDWR)
    if self.socket:
      self.socket.close()
    super().reset()
        
