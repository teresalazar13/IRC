#!/usr/bin/python           # This is server.py file

import socket               # Import socket module
import sys
import json


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
        try:
            request = client.recv(1024)
        except KeyboardInterrupt:
            sys.exit(1)
            client.close()
        option = request.decode("utf-8")
        if option == "0":
            user = request.decode("utf-8")
        if option == "8":
            print("Client with address", address, " closed connection")
            client.close()


def main():
    print("Hello World")
    server(9000)


if __name__ == '__main__':
    main()
