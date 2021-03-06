import asyncio
from itertools import chain


class Protocol(asyncio.Protocol):

    def __init__(self, chat_room):
        self._chat_room = chat_room
        self._username = None
        self._transport = None
        self._buffer = []

    def connection_made(self, transport):
        self._transport = transport
        print('New client connected')
        self._write("Enter username: ")

    def data_received(self, raw_data):
        try:
            data = raw_data.decode('utf-8')
        except UnicodeDecodeError as e:
            self._transport._write(str(e).encode('utf-8'))
        else:
            for line in self._accumulated_lines(data):
                self._handle(line)

    def connection_lost(self, exc):
        self._deregister_user()

    def _accumulated_lines(self, data):
        self._buffer.append(data)
        while True:
            tail, newline, head = self._buffer[-1].partition('\n')
            if not newline:
                break
            line = ''.join(chain(self._buffer[:-1], (tail,)))
            self._buffer = [head]
            yield line

    def _handle(self, line):
        if self._username is None:
            self._register_user(line)
        elif line == "NAMES":
            self._list_users()
        else:
            self._chat_room.message_from(self._username, line)

    def _register_user(self, line):
        username = line.strip()
        self._writeline("\n------------------------------------")
        if self._chat_room.register_user(username, self._transport):
            self._username = username
        else:
            self._writeline("Username {} not available".format(username))
        self._list_users()

    def _deregister_user(self):
        if self._username is not None:
            self._chat_room.deregister_user(self._username)

    def _list_users(self):
        self._writeline("Currently connected users: ")
        self._write(', '.join(self._chat_room.users()))
        self._writeline("")

    def _writeline(self, line):
        self._write(line)
        self._write('\n')

    def _write(self, text):
        self._transport.write(text.encode('utf-8'))
