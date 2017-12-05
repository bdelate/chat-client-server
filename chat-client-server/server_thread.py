import socket
from threading import Thread


def on_new_client(client_socket, address):
    connected = True
    while connected:
        message = client_socket.recv(1024)
        message = message.decode('utf-8')
        message = message.rstrip('\n')
        if message == '\q':
            break
        print(address, ' >> ', message)
        client_socket.sendall('return message from server'.encode('utf-8'))
    client_socket.close()


s = socket.socket()
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
host = socket.gethostname()
port = 9009

print('Server started!')

s.bind((host, port))
s.listen(5)

while True:
    client_socket, address = s.accept()
    print('Got connection from', address)
    client_thread = Thread(target=on_new_client, args=(client_socket, address))
    client_thread.start()
s.close()
