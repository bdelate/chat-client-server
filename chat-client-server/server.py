from mode_thread import server as thread_server
from mode_asyncio import server as asyncio_server


if __name__ == '__main__':
    mode = input('Server mode (enter "t" or "a"):\nt: Threads\na: Asyncio\n> ')
    if mode == 't':
        thread_server.start_server()
    elif mode == 'a':
        asyncio_server.start_server()
    else:
        print('Invalid server mode (enter "t" or "a")')
