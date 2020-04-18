# Chat Room
This TCP Chat Room supports one-to-one and one-to-all messaging. Other features include querying other active users and accessing the help menu.

## Get Started

### Server
You must run the server before any of the clients. Use the following command:
```
python2 server.py 127.0.0.1 1234
```
This chat room is built in python 2, and will not work in python 3. The arguments on the command line are IP address and port. for ease, use localhost (127.0.0.1) and any Port you like (1234).
The server creates a new thread for each client in the chat room. It receives messages and commands from all its different client threads, and distributes them according to their specifications.

### Client
You can run as many as 100 clients at a time on the server. Use the following command:
```
python2 client.py 127.0.0.1 1234 johnsmith
```
The arguments on the command line are IP address, port, and username. Make sure the IP address and port are the same as those given to the server. Username can be anything you like.
Each client waits to receive messages distributed from the server, or to send messages created by the client. If the client receives a message, it is displayed on the user interface. If the user wants to send a message or use any other command, it is sent to the server for proper distribution.

## Functions
All client actions are executed with ```ENTER``` from the command line.

### One-To-Many Messaging

If you desire to send a message to the entire chat room, simply type the message on the command line. This function can be found in ```server.py```, named ```broadcast()```. This function accepts the message and distributes it to all users in the chat room.

### One-To-One Messaging

If you would like to send a message to one user that will be hidden from everyone else in the chat room, type '@' followed by their username and a space, then type your message. For example:
```
@johnsmith Top of the mornin' to ya lad
```
This function can be found in ```server.py```, named ```private_message()```. This function accepts the message, finds the desired user, and distributes it to only the intended recipient.

### Query User List
If you would like to see a list of active users, type ```*users```. This returns a list of the form:
```
User List:
[1] johnsmith
[2] johndoe
[3] janedoe
```
This function can be found in ```server.py```, named ```user_list()```. This function constructs a list of active users and returns it to the client.
### Help
If you need to be reminded of the functions available to you, type ```*help```. This function can be found in ```server.py```, named ```help()```. This function returns a help message to the client.

### Exit
If you wish to exit the chat room, type ```ctrl + C``` to interrupt the connection.
