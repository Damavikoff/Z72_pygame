import socket as sck
from socket import socket
from ..defaults import HOST, PORT
from threading import Thread

class SocketServer(Thread):
  def __init__(self) -> None:
      self.is_up = False
      self.data = None
      self.error = None
      self.socket: socket | None
      super().__init__(target = self.start_t, daemon = True)

  def start_t(self) -> None:
    if self.is_up: return
    try:
      with socket(sck.AF_INET, sck.SOCK_STREAM) as s:
        self.socket = s
        s.bind((HOST, PORT))
        s.listen(1)
        conn, addr = s.accept()
        self.is_up = True
        with conn:
          print('Connection established: ', addr)
          while True:
            if not self.is_up:
              break
            data = conn.recv(1024)
            if data:
              print('###', data.decode())
              conn.sendall(data)
            else:
              break
    except Exception as e:
      print(e)
      self.error = e
    finally:
      self.stop()


  def stop(self) -> None:
    if self.socket: self.socket.close()
    self.socket = None
    self.error = None
    self.is_up = False
    self.data = None