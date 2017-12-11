import socket
import select
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock.bind(('96.126.109.157', 8453))
sock.listen(5)

# lists of sockets to watch for input and output events
ins = [sock]
ous = []
# mapping socket -> data to send on that socket when feasible
data = {}
# mapping socket -> (host, port) on which the client is running
adrs = {}

try:
    while True:
        i, o, e = select.select(ins, ous, [])  # no excepts nor timeout
        for x in i:
            if x is sock:
                # input event on sock means client trying to connect
                newSocket, address = sock.accept()
                print("Connected from", address)
                ins.append(newSocket)
                adrs[newSocket] = address
            else:
                # other input events mean data arrived, or disconnections
                newdata = x.recv(8192)
                if newdata:
                    newdata = newdata.decode('utf-8')
                    # data arrived, prepare and queue the response to it
                    print("%d bytes from %s" % (len(newdata), adrs[x]))
                    data[x] = data.get(x, '') + newdata
                    if x not in ous:
                        ous.append(x)
                else:
                    # a disconnect, give a message and clean up
                    print("disconnected from", adrs[x])
                    del adrs[x]
                    ins.remove(x)
                    try:
                        ous.remove(x)
                    except ValueError:
                        pass
                    x.close()
        for x in o:
            # output events always mean we can send some data
            tosend = data.get(x)
            if tosend:
                nsent = x.send(tosend.encode('utf-8'))
                print("%d bytes to %s" % (nsent, adrs[x]))
                # remember data still to be sent, if any
                tosend = tosend[nsent:]
            if tosend:
                print("%d bytes remain for %s" % (len(tosend), adrs[x]))
                data[x] = tosend
            else:
                try:
                    del data[x]
                except KeyError:
                    pass
                ous.remove(x)
                print("No data currently remain for", adrs[x])
finally:
    sock.close()


# import asyncore
# import socket
#
#
# class MainServerSocket(asyncore.dispatcher):
#
#     def __init__(self, port):
#         asyncore.dispatcher.__init__(self)
#         self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
#         self.bind(('', port))
#         self.listen(5)
#
#     def handle_accept(self):
#         newSocket, address = self.accept()
#         print("Connected from", address)
#         SecondaryServerSocket(newSocket)
#
#
# class SecondaryServerSocket(asyncore.dispatcher_with_send):
#     def handle_read(self):
#         receivedData = self.recv(8192)
#         if receivedData:
#             self.send(receivedData)
#         else:
#             self.close()
#
#     def handle_close(self):
#         print("Disconnected from", self.getpeername())
#
#
# MainServerSocket(9009)
# asyncore.loop()
