# chat-client-server
Python based chat client / server using either Asyncio or Threads

### Overview
This is a basic chat client / server demonstrating the differences when using an Asyncio versus a Threaded implementation.

### Requirements
Python 3.5+

### Usage (Threads)
1. Start the server `python server.py`
2. Select Thread mode
3. Start the client in a different terminal (either on the same computer or a different one) `python client.py`
4. Start another client
5. You now have two clients connected to the server which can chat to each other
6. To quit the client, type `\q`

### Usage (Asyncio)
1. Start the server `python server.py`
2. Select Asyncio mode
3. Open a new terminal on the same or a different computer. Telnet into the server on port 8453 `telnet ipaddress 8453`
4. Enter a username
5. Connect another client (ie: telnet) and enter another username
6. You now have two clients connected to the server which can chat to each other

### Notes
This is not meant to be a full featured chat client/server but is simply meant to demonstrate an Ayncio vs Threaded implementation.

### To do:
Create a client for the Asyncio version so that telnet is not needed
