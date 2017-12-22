import asyncio
from .protocol import Protocol


class ChatRoom:

    def __init__(self, port, loop):
        self._port = port
        self._loop = loop
        self._username_transports = {}

    def run(self):
        print('The server is running. Awaiting client connections...')
        coro = self._loop.create_server(
            protocol_factory=lambda: Protocol(self),
            host="",
            port=self._port
        )
        return self._loop.run_until_complete(coro)

    def register_user(self, username, transport):
        if username in self.users():
            return False
        self._username_transports[username] = transport
        self._broadcast("User {} arrived".format(username))
        return True

    def deregister_user(self, username):
        del self._username_transports[username]
        self._broadcast("User {} departed".format(username), username)

    def users(self):
        return self._username_transports.keys()

    def message_from(self, username, message):
        self._broadcast("{}: {}".format(username, message), username)

    def _broadcast(self, message, username=None):
        for user, transport in self._username_transports.items():
            if user != username:
                transport.write(message.encode('utf-8'))
                transport.write('\n'.encode('utf-8'))


def start_server():
    loop = asyncio.get_event_loop()
    chat_room = ChatRoom(8453, loop)
    _ = chat_room.run()
    loop.run_forever()
