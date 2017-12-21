from mode_thread import server as thread_server
from mode_asyncio import server as asyncio_server
import asyncio


if __name__ == '__main__':
    mode = input('Server mode (enter "t" or "a"):\nt: Threads\na: Asyncio\n> ')
    if mode == 't':
        thread_server.start_server()
    elif mode == 'a':
        loop = asyncio.get_event_loop()
        loop.run_until_complete(asyncio_server.start_server(loop))
    else:
        print('Invalid server mode (enter "t" or "a")')
