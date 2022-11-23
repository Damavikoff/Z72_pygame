import socket as sock

HOST = '127.0.0.1'    # The remote host
PORT = 50007              # The same port as used by the server
with sock.socket(sock.AF_INET, sock.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    s.sendall(b'Hello, world')
    data = s.recv(1024)
    print('Received', repr(data))
    print('x-1')
    s.sendall(b'Hello, winter!')
    print('x-2')
    data = s.recv(1024)
    print('x-3')
    print('Received', repr(data))
print('completed')
