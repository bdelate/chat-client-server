from mode_thread import client


if __name__ == '__main__':
    host = input('Enter host name or ip address: ')
    client.start_client(host=host)
