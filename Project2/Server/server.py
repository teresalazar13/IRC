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
    print "Socket creation successfull"
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
        if option == "8":
            print "Client with address", address, "closed connection"
            client.close()
            return
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
            client.send("1".encode("utf-8"))
        else:
            client.send("0".encode("utf-8"))
    elif option == "2":
        list_of_clients = list_clients()
        client.send(list_of_clients.encode("utf-8"))
    elif option == "3":
        send_message(client, address)


def check_user(user):
    file = open("clients.txt", "r")
    for line in file:
        line = line.strip("\n")
        separated_info = line.split(',')
        if separated_info[0] == user[0] and separated_info[1] == user[1]:
            file.close()
            return True
    file.close()
    return False


def list_clients():
    users = ""
    file = open("clients.txt", "r")
    for line in file:
        line = line.strip("\n")
        separated_info = line.split(',')
        users += separated_info[0] + "\n"
    file.close()
    return users


def send_message(client, address):
    try:
        request = client.recv(1024)
    except KeyboardInterrupt:
        sys.exit(1)
        client.close()
    message = request.decode("utf-8")
    message = json.loads(message)
    if check_username(message[2]):
        client.send("1".encode("utf-8"))
        write_message(message)
    else:
        client.send("0".encode("utf-8"))
        return


def check_username(username):
    file = open("clients.txt", "r")
    for line in file:
        line = line.strip("\n")
        separated_info = line.split(',')
        if separated_info[0] == username:
            file.close()
            return True
    file.close()
    return False


def write_message(message):
    file = open("messages.txt", "a")
    file.write(message[0] + "|" + message[1] + "|" + message[2] + "\n")
    file.close()


def main():
    print "Hello World"
    server(9000)


if __name__ == '__main__':
    main()
