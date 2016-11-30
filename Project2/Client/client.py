#!/usr/bin/python           # This is client.py file

import socket               # Import socket module
import sys


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
    users_and_files = {}
    loggedin_user = []
    server_port = 9000
    conn = create_socket(server_port)

    while True:
        choice = menu()
        conn.send(choice.encode("utf-8"))


def menu():
    option = input("1 LIST_MESS - para listar todas as mensagens por ler.\n2 LIST_USERS - para listar todos os clientes autorizados.\n3 SEND_MESS - para enviar uma mensagem para um cliente (autorizado).\n4 LIST_READ - para listar todas as mensagens ja lidas.\n5 REMOVE_MES - para apagar mensagens.\n6 CHANGE_PASSW - alterar a password\n7 OPER - para o cliente obter os privilegios do operador.\n8 QUIT - para o cliente abandonar o sistema.\n")
    return str(option)


if __name__ == '__main__':
    main()
