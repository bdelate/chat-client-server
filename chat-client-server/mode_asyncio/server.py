import socket
import asyncio


async def start_server(loop):
    connected_client_sockets = []
    # client_manager_lock = Lock()
    client_manager_lock = None
    server_socket = create_server_socket()

    while True:
        client_socket, address = await loop.sock_accept(server_socket)
        client_socket.settimeout(20)  # ping client every 20 seconds using client_still_connected() to see if they're still connected
        print('Client connected from:', address)
        loop.create_task(client_manager(client_socket, address, client_manager_lock, connected_client_sockets, loop))
        # client_thread = Thread(target=client_manager, args=(client_socket, address, client_manager_lock, connected_client_sockets))
        # client_thread.daemon = True
        # client_thread.start()
        #
        # with client_manager_lock:
        #     connected_client_sockets.append(client_socket)
    server_socket.close()


async def client_manager(client_socket, address, client_manager_lock, connected_client_sockets, loop):
    is_connected = True
    while is_connected:
        message = await loop.sock_recv(client_socket, 1024)
        if message:
            print(message.decode('utf-8'))
        # except socket.timeout:
        #     pass
            # is_connected = client_still_connected(client_socket=client_socket, address=address)
        # else:
        #     if message:
        #         print(message.decode('utf-8'))
    #             message = message.decode('utf-8')
    #             message = message.rstrip('\n')
    #             if message == '\q':
    #                 print('Client disconnected from:', address)
    #                 is_connected = False
    #             else:
    #                 broadcast_message(message=message,
    #                                   originator=client_socket,
    #                                   client_manager_lock=client_manager_lock,
    #                                   connected_client_sockets=connected_client_sockets)
    #
    #         else:
    #             is_connected = client_still_connected(client_socket=client_socket, address=address)
    #
    # with client_manager_lock:
    #     connected_client_sockets.remove(client_socket)
    # client_socket.close()


def broadcast_message(message, originator, client_manager_lock, connected_client_sockets):
    with client_manager_lock:
        for client in connected_client_sockets:
            if client != originator:
                try:
                    client.sendall(message.encode('utf-8'))
                except socket.error:
                    print('Broadcast message failed to:', client)


def client_still_connected(client_socket, address):
    try:
        client_socket.sendall('<ping>'.encode('utf-8'))
    except socket.error:
        print('Client has disconnected unexpectedly:', address)
        return False
    else:
        return True


def create_server_socket():
    server_socket = socket.socket()
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    host = socket.gethostname()
    port = 8453
    server_socket.bind((host, port))
    server_socket.listen(5)
    server_socket.setblocking(False)
    print('The server has started and is listening for client connections')
    return server_socket
