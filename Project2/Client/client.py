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
    while True:
        try:
            option = menu()
            if option == "0":
                user = login()
                conn.send(option.encode("utf-8"))
                conn.send(user.encode("utf-8"))
            elif option == "1":
                conn.send(option.encode("utf-8"))
            elif option == "2":
                conn.send(option.encode("utf-8"))
            elif option == "3":
                conn.send(option.encode("utf-8"))
            elif option == "4":
                conn.send(option.encode("utf-8"))
            elif option == "5":
                conn.send(option.encode("utf-8"))
            elif option == "6":
                conn.send(option.encode("utf-8"))
            elif option == "7":
                conn.send(option.encode("utf-8"))
            elif option == "8":
                conn.send(option.encode("utf-8"))
                close_connection(conn)
                return
            else:
                print("Invalid option")
        except KeyboardInterrupt:
            close_connection(conn)


def menu():
    option = input("1 - Listar todas as mensagens por ler\n"
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
    return request


def close_connection(conn):
    conn.close()
    sys.exit(1)

if __name__ == '__main__':
    main()
