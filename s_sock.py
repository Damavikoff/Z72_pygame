import socket
import asyncio
from src.classes.c_server import SocketServer
from src.classes.c_client import SocketClient
from time import sleep
import keyboard

server = SocketServer()
client = SocketClient()

def blah():
  print(1)

async def main():
    task = asyncio.create_task(server.start())
    task.add_done_callback(lambda x: print('Server is Done'))
    await task

server.start()
# asyncio.run(main())
# server.start()
client.start()
client.send('hello')
client.send('hi')
sleep(3)
client.stop()
  
print('Done')

# task = asyncio.create_task(blah())
# task.add_done_callback(lambda : print('Server is Done'))
# asyncio.run(task)
