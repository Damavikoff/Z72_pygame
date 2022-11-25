import socket
import asyncio
from src.classes.c_server import SocketServer
from src.classes.c_client import SocketClient
from time import sleep

def client_handler(data):
  print('client request is ', data)

def server_handler(data):
  print('server request is ', data)

server = SocketServer(handler = client_handler)
client = SocketClient(handler = server_handler)


# server.start()
# client.start()
# sleep(1)
# server.send('act 3')
# client.send('act 3')
# sleep(1)
# client.is_up = False
# print('stopped')
# client.reset()
# server.reset()
# # sleep(1)
# client.start()
# # server.start()
# sleep(1)
# client.send('# after restart')
# sleep(1)
# server.reset()
# sleep(1)
server.start()
sleep(1)
server.unset()
sleep(1)
print('Done')

# task = asyncio.create_task(blah())
# task.add_done_callback(lambda : print('Server is Done'))
# asyncio.run(task)
