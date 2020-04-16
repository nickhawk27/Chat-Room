import socket
import select
from _thread import *
import sys

help_message = ("\nWelcome to the help menu:\n\n"
                "Private Message: Type '@' followed by the user's name to send a private message. \n"
                "Make sure to leave a space before you start your message to the desired recipient.\n\n"
                "View Users: Type '*users' to receive a list of the other users in the chat room.\n\n"
                "Exit: Type '*exit' to leave the chat room\n")

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

if len(sys.argv) != 3:
    print("Correct usage: script, IP address, port number")
    exit()

IP = str(sys.argv[1])
PORT = int(sys.argv[2])
server.bind((IP, PORT))

server.listen(100)
clients = {}

def clientthread(connection, address):
    connection.send("Welcome to this chatroom, {}! Type '*help' to see more options.".format(get_user(connection)))
    #sends a message to the client whose user object is conn
    while True:
            try:
                message = connection.recv(2048)
                if message:
                    if message[0:len(message)-1] == "*help":
                        print("help")
                        help(connection)
                    elif message[0] == "@":
                        print("private message")
                        private_message(get_user(connection), message)
                    elif message[0:len(message)-1] == "*users":
                        print("user list")
                        user_list(connection)
                    elif message[0:len(message)-1] == "*exit":
                        exit_client(connection)
                    else:
                        broadcast(connection, message)
                    #prints the message and address of the user who just sent the message on the server terminal
                else:
                    remove(connection)
            except:
                continue

def broadcast(connection, message):
    message_final = "<" + get_user(connection) + "> " + message
    for client in clients.keys():
        if client != connection:
            try:
                client.send(message_final)
            except:
                client.close()
                remove(client)

def private_message(connection, message):
    # Construct username to send message to
    recipient_name = ""
    for i in range(1, len(message)):
        if not message[i].isspace():
            recipient_name += message[i]
        else:
            break
    # Find user
    for connection, username in clients.items():
        if username == recipient_name:
            recipient = connection
            break
    direct_message = "<{}> (Private Message) {}".format(username, message[i+1:len(message)-1])
    try:
        recipient.send(direct_message)
    except:
        connection.send("User does not exist.")

def help(connection):
    try:
        connection.send(help_message)
    except:
        connection.close()
        remove(connection)

def user_list(connection):
    i = 1
    users = "User List:\n"
    for client in clients.values():
        users += "[{}] {}\n".format(i, client)
        i += 1
    try:
        connection.send(users)
    except:
        connection.close()
        remove(connection)

def exit_client(connection):
    connection.close()
    remove(connection)

def remove(connection):
    del clients[connection]

def get_user(connection):
    return clients[connection]

# Continuously accepts new users
while True:
    connection, address = server.accept()
    # Immediately accept username
    username = connection.recv(2048)
    # Append to list of clients
    clients[connection] = username
    print(username + " connected")
    # Creates a new thread for every player that connects
    start_new_thread(clientthread,(connection,address))

connection.close()
server.close()
