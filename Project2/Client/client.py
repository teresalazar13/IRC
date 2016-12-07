import socket
import sys
import json
import getopt
import getpass


def client(server_port):
    conn = create_socket(server_port)
    user = []
    while True:
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
        elif option in ["2", "4", "5", "6", "7", "8"] and (user == [] or user == None):
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
                enter_superuser_mode(conn, user)
            else:
                print "Invalid option"


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
    option = raw_input("0 - Register\n"
                   "1 - Login\n"
                   "2 - List unread messages\n"
                   "3 - List authorized clients\n"
                   "4 - Send a message to a client\n"
                   "5 - List read messages\n"
                   "6 - Delete a message\n"
                   "7 - Change password\n"
                   "8 - Get operator privileges\n"
                   "9 - Quit\n")
    return str(option)


def menu_superuser():
    option = raw_input("1 - Remove a client from database\n"
                   "2 - Remove a message\n"
                   "3 - Quit superuser mode\n")
    return str(option)


def register(conn):
    username = ""
    while 0 == len(username) or len(username) >= 9:
        username = raw_input("Username (max length 9): ")
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
    message_number = raw_input("Which message do you want do delete? Please select a number: ")
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


def enter_superuser_mode(conn, user):
    user = json.dumps(user)
    conn.send(user.encode("utf-8"))
    client_is_superuser = conn.recv(1024).decode("utf-8")
    if client_is_superuser == "1":
        print "You are now in superuser mode"
    else:
        print "You are not a superuser"
        option = raw_input("Do you want to become superuser? (y/n): ")
        if option == "n":
            conn.send("0".encode("utf-8"))
            return
        elif option == "y":
            conn.send("1".encode("utf-8"))
            password = getpass.getpass()
            conn.send(password.encode("utf-8"))
            check_password = conn.recv(1024).decode("utf-8")
            if check_password == "1":
                print "You are now a superuser"
            else:
                print "Wrong password"
                return
        else:
            conn.send("0".encode("utf-8"))
            print "Invalid input"
            return
    while True:
        option = menu_superuser()
        conn.send(option.encode("utf-8"))
        if option == "1":
            client_to_remove = raw_input("Which client do you want to remove: ")
            conn.send(client_to_remove.encode("utf-8"))
        elif option == "2":
            superuser_deletes_message(conn, user)
        elif option == "3":
            print "Quitting superuser mode"
            return
        else:
            print "Invalid option"


def superuser_deletes_message(conn, user):
    all_messages = conn.recv(1024).decode("utf-8")
    print all_messages
    message = raw_input("Which message do you want to delete: ")
    conn.send(str(message).encode("utf-8"))
    check = conn.recv(1024).decode("utf-8")
    if check == "1":
        print "Message was deleted successfully"
    else:
        print "Could not delete the message"


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
