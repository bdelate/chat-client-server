import sys
import socket
import select


def chat_client():
    if(len(sys.argv) < 3):
        print('Usage : python client.py hostname port')
        sys.exit()

    host = sys.argv[1]
    port = int(sys.argv[2])

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # connect to remote host
    try:
        s.connect((host, port))
    except:
        print('Unable to connect')
        sys.exit()

    print('Connected to remote host. You can start sending messages')
    sys.stdout.write('[Me] ')
    sys.stdout.flush()

    while 1:
        socket_list = [sys.stdin, s]

        # Get the list sockets which are readable
        ready_to_read, ready_to_write, in_error = select.select(socket_list, [], [])

        for sock in ready_to_read:
            if sock == s:
                # incoming message from remote server, s
                data = sock.recv(4096)
                if data:
                    message = data.decode('utf-8')
                    if message != '<ping>':
                        sys.stdout.write(message)
                        sys.stdout.write('[Me] ')
                        sys.stdout.flush()
            else:
                # user entered a message
                msg = sys.stdin.readline()
                s.sendall(msg.encode('utf-8'))
                sys.stdout.write('[Me] ')
                sys.stdout.flush()


if __name__ == "__main__":

    sys.exit(chat_client())