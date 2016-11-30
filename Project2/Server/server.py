#!/usr/bin/python           # This is server.py file

import socket               # Import socket module


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
        print "Connected"


def main():
    print "Hello World"
    server(9000)


if __name__ == '__main__':
    main()
