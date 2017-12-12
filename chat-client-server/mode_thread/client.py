import sys
import socket
from threading import Thread


def start_client(host):
    client_socket = connect(host=host)
    response_thread = Thread(target=server_response_monitor, args=(client_socket,))
    response_thread.daemon = True
    response_thread.start()

    input_thread = Thread(target=input_monitor, args=(client_socket,))
    input_thread.daemon = True
    input_thread.start()

    response_thread.join()
    input_thread.join()


def connect(host):
    port = 8453

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.settimeout(20)  # ping server every 20 seconds using server_still_connected() to see if client still connected

    # connect to remote host
    try:
        client_socket.connect((host, port))
    except:
        print('Unable to connect')
        sys.exit()

    print('Connection established.')
    return client_socket


def server_response_monitor(client_socket):
    is_connected = True
    while is_connected:
        try:
            message = client_socket.recv(1024)
        except socket.timeout:
            is_connected = server_still_connected(client_socket=client_socket)
        else:
            if message:
                message = message.decode('utf-8')
                message = message.rstrip('\n')
                if message != '<ping>':
                    print(message)
            else:
                print('Server connection lost. You have been disconnected.')
                is_connected = False
    client_socket.close()


def input_monitor(client_socket):
    while True:
        message = input('')
        try:
            client_socket.sendall(message.encode('utf-8'))
        except socket.error:
            break
        else:
            if message == '\q':
                break


def server_still_connected(client_socket):
    try:
        client_socket.sendall('<ping>'.encode('utf-8'))
    except socket.error:
        print('Server connection lost. You have been disconnected.')
        return False
    else:
        return True
