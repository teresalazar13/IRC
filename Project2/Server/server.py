#!/usr/bin/python           # This is server.py file

import socket               # Import socket module
import sys
import json
import thread


def create_socket(port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    host = socket.gethostname()
    s.bind((host, port))
    s.listen(5)
    print("Socket creation successfull")
    return s


def server(port):
    server_socket = create_socket(port)
    print "The server is ready to receive"
    while True:
        client, address = server_socket.accept()
        thread.start_new_thread(process_client, (client, address))


def process_client(client, address):
    while True:
        try:
            request = client.recv(1024)
        except KeyboardInterrupt:
            sys.exit(1)
            client.close()
        option = request.decode("utf-8")
        process_client_request(client, address, option)


def process_client_request(client, address, option):
    if option == "0":
        try:
            request = client.recv(1024)
        except KeyboardInterrupt:
            sys.exit(1)
            client.close()
        user = request.decode("utf-8")
        user = json.loads(user)
        if check_user(user) == True:
            print "User is valid"
            client.send("1".encode("utf-8"))
        else:
            print "User is not valid"
            client.send("0".encode("utf-8"))
    if option == "8":
        print("Client with address", address, " closed connection")
        client.close()


def check_user(user):
    file = open("dataBase.txt", "r")
    for line in file:
        line = line.strip("\n")
        separated_info = line.split(',')
        if separated_info[0] == user[0] and separated_info[1] == user[1]:
            file.close()
            return True
    file.close()
    return False


def main():
    print("Hello World")
    server(9000)


if __name__ == '__main__':
    main()
