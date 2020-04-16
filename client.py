import socket
import select
import sys

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
if len(sys.argv) != 4:
    print("Correct usage: script, IP address, port number, username")
    exit()

IP = str(sys.argv[1])
PORT = int(sys.argv[2])
USERNAME = str(sys.argv[3])
server.connect((IP, PORT))
server.send(USERNAME)

while True:
    sockets_list = [sys.stdin, server]
    read_sockets, write_socket, error_socket = select.select(sockets_list, [], [])
    for socket in read_sockets:
        if socket == server:
            message = socket.recv(2048)
            print(message)
        else:
            message = sys.stdin.readline()
            server.send(message)
            personal_message = "<You> {}\n".format(message)
            sys.stdout.write(personal_message)
            sys.stdout.flush()
server.close()
