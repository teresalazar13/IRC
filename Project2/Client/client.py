import socket
import sys
import json
import getopt


def client(server_port):
    conn = create_socket(server_port)
    user = []
    while True:
        try:
            option = menu()
            if option == "0":
                conn.send(option.encode("utf-8"))
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
            elif option == "2":
                conn.send(option.encode("utf-8"))
                print "LIST OF AUTHORIZED CLIENTS"
                print conn.recv(1024).decode("utf-8")
            elif option == "8":
                conn.send(option.encode("utf-8"))
                close_connection(conn)
                return
            elif option in ["1", "3", "4", "5", "6", "7"] and user == []:
                print "Please login first"
            else:
                conn.send(option.encode("utf-8"))
                if option == "1":
                    list_messages(conn, user, 0)
                elif option == "3":
                    send_message(conn, user)
                elif option == "4":
                    list_messages(conn, user, 1)
                elif option == "5":
                    delete_message(conn, user)
                elif option == "6":
                    change_password(conn, user)
                elif option == "7":
                    print "oi"
                else:
                    print "Invalid option"
        except KeyboardInterrupt:
            close_connection(conn)


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


def menu():
    option = input("0 - Login\n"
                    "1 - Listar todas as mensagens por ler\n"
                    "2 - Listar todos os clientes autorizados\n"
                    "3 - Enviar uma mensagem para um cliente (autorizado)\n"
                    "4 - Listar todas as mensagens ja lidas\n"
                    "5 - Apagar mensagens\n"
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
        if read == 2:
            print "There are no messages to delete"
            return False


def send_message(conn, user):
    receiver = input("Who do you wish to send your message? ")
    message_text = input("Please write your message: ")
    message = [user[0], message_text, receiver]
    message = json.dumps(message)
    conn.send(message.encode("utf-8"))
    if conn.recv(1024).decode("utf-8") == "1":
        print "Message was sent to", receiver
    else:
        print "Can't send message to", receiver, ". User is not valid."


def delete_message(conn, user):
    if list_messages(conn, user, 2) == False or user == []:
        return
    message_number = input("Which message do you want do delete? Please select a number: ")
    conn.send(str(message_number).encode("utf-8"))
    check = conn.recv(1024).decode("utf-8")
    if check == "1":
        print "Message deleted successfully"
    elif check == "0":
        print "Could not delete the desired message. The message you chose is not yours to delete."
    else:
        print "Invalid input."


def change_password(conn, user):
    new_password = input("Please enter new password: ")
    user = [user[0], new_password]
    user = json.dumps(user)
    conn.send(user.encode("utf-8"))
    print "Password was changed successfully"


def close_connection(conn):
    conn.close()
    sys.exit(1)


def main(argv):
    print "Hello World"
    port = ''
    try:
        opts, args = getopt.getopt(argv, "hp:", ["pport="])
    except getopt.GetoptError:
        print 'client.py -p <port>'
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print 'client.py -p <port>'
            sys.exit()
        elif opt in ("-p", "--pport"):
            port = arg
    if port != "":
        client(int(port))
    else:
        print 'ERROR - Usage: client.py -p <port>'
        return


if __name__ == '__main__':
    main(sys.argv[1:])
