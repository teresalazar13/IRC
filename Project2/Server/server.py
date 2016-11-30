#!/usr/bin/python           # This is server.py file

import socket               # Import socket module
import sys


def create_socket(port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    host = socket.gethostname()
    s.bind((host, port))
    s.listen(5)
    print("Socket creation successfull")
    return s


def server(port):
    server_socket = create_socket(port)
    client, address = server_socket.accept()
    print "The server is ready to receive"

    while True:
        try:
            request = client.recv(1024)
        except KeyboardInterrupt:
            s.close()
            sys.exit(1)
        option = request.decode("utf-8")
        print option


def main():
    print "Hello World"
    server(9000)


if __name__ == '__main__':
    main()
