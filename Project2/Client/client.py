import socket
import sys
import json
import getopt
import getpass


def client(server_port):
    conn = create_socket(server_port)
    user = []
    while True:
        try:
            option = menu()
            if option == "0":
                conn.send(option.encode("utf-8"))
                user = register(conn)
            elif option == "1":
                conn.send(option.encode("utf-8"))
                user = login(conn)
            elif option == "3":
                conn.send(option.encode("utf-8"))
                print "LIST OF AUTHORIZED CLIENTS"
                print conn.recv(1024).decode("utf-8")
            elif option == "9":
                conn.send(option.encode("utf-8"))
                close_connection(conn)
                return
            elif option in ["2", "4", "5", "6", "7", "8"] and user == []:
                print "Please login first"
            else:
                conn.send(option.encode("utf-8"))
                if option == "2":
                    list_messages(conn, user, 0)
                elif option == "4":
                    send_message(conn, user)
                elif option == "5":
                    list_messages(conn, user, 1)
                elif option == "6":
                    delete_message(conn, user)
                elif option == "7":
                    change_password(conn, user)
                elif option == "8":
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
    option = input("0 - Registar\n"
                   "1 - Login\n"
                   "2 - Listar todas as mensagens por ler\n"
                   "3 - Listar todos os clientes autorizados\n"
                   "4 - Enviar uma mensagem para um cliente (autorizado)\n"
                   "5 - Listar todas as mensagens ja lidas\n"
                   "6 - Apagar mensagens\n"
                   "7 - Alterar a password\n"
                   "8 - Obter privilegios do operador\n"
                   "9 - Abandonar o sistema\n")
    return str(option)


def register(conn):
    username = raw_input("Username: ")
    password = getpass.getpass()
    user = [username, password]
    request = json.dumps(user)
    conn.send(request.encode("utf-8"))
    print "Register successfull. Welcome", username, "!"
    return user


def login(conn):
    username = raw_input("Username: ")
    password = getpass.getpass()
    user = [username, password]
    request = json.dumps(user)
    conn.send(request.encode("utf-8"))
    check_user = conn.recv(1024).decode("utf-8")
    if check_user == "1":
        print "Welcome", user[0], "!"
        return user
    else:
        print "Username or password incorrect"


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
    receiver = raw_input("Who do you wish to send your message? ")
    message_text = raw_input("Please write your message: ")
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
    new_password = getpass.getpass()
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
