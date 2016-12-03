#!/usr/bin/python           # This is client.py file

import socket               # Import socket module
import sys
import json


def create_socket(port):
    try:
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    except socket.error as e:
        print(e)
        sys.exit(1)
    host = socket.gethostname()
    try:
        client_socket.connect((host, port))
    except socket.error as e:
        print(e)
        sys.exit(1)
    print("Socket created successfully")
    return client_socket


def main():
    server_port = 9000
    conn = create_socket(server_port)
    user = []
    while True:
        try:
            option = menu()
            conn.send(option.encode("utf-8"))
            if option == "0":
                user_login = login()
                user_string = user_login[0]
                user_array = user_login[1]
                conn.send(user_string.encode("utf-8"))
                check_user = conn.recv(1024).decode("utf-8")
                if check_user == "1":
                    print "Welcome", user_array[0], "!"
                    user = user_array
                else:
                    print "Username or password incorrect"
            elif option == "1":
                list_messages(conn, user, 0)
            elif option == "2":
                print "LIST OF AUTHORIZED CLIENTS"
                print conn.recv(1024).decode("utf-8")
            elif option == "3":
                send_message(conn, user)
            elif option == "4":
                list_messages(conn, user, 1)
            elif option == "5":
                print "oi"
            elif option == "6":
                print "oi"
            elif option == "7":
                print "oi"
            elif option == "8":
                close_connection(conn)
                return
            else:
                print("Invalid option")
        except KeyboardInterrupt:
            close_connection(conn)


def menu():
    option = input("0 - Login\n"
                    "1 - Listar todas as mensagens por ler\n"
                    "2 - Listar todos os clientes autorizados\n"
                    "3 - Enviar uma mensagem para um cliente (autorizado)\n"
                    "4 - Listar todas as mensagens ja lidas.\n"
                    "5 - Apagar mensagens.\n"
                    "6 - Alterar a password\n"
                    "7 - Obter privilegios do operador\n"
                    "8 - Abandonar o sistema\n")
    return str(option)


def login():
    username = input("Username: ")
    password = input("Password: ")
    user = [username, password]
    request = json.dumps(user)
    return [request, user]


def list_messages(conn, user, read):
    if user == []:
        print "Please login first"
        return
    conn.send(user[0].encode("utf-8"))
    messages = conn.recv(1024).decode("utf-8")
    if messages != "0":
        print "LIST OF YOUR MESSAGES"
        print messages
    else:
        if read == 0:
            print "You have no unread messages"
        if read == 1:
            print "You have no read messages"

def send_message(conn, user):
    if user == []:
        print "Please login first"
        return
    receiver = input("Who do you wish to send your message? ")
    message_text = input("Please write your message: ")
    message = [user[0], message_text, receiver]
    message = json.dumps(message)
    conn.send(message.encode("utf-8"))
    if conn.recv(1024).decode("utf-8") == "1":
        print "Message was sent to", receiver
    else:
        print "Can't send message to", receiver, ". User is not valid."


def close_connection(conn):
    conn.close()
    sys.exit(1)


if __name__ == '__main__':
    main()
