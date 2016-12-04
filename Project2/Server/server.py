import socket
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
    elif option == "1":
        username = list_messages_client(client, address, 0)
        mark_messages_read(client, address, username)
    elif option == "2":
        list_of_clients = list_clients()
        client.send(list_of_clients.encode("utf-8"))
    elif option == "3":
        send_message(client, address)
    elif option == "4":
        username = list_messages_client(client, address, 1)
    elif option == "5":
        delete_message(client, address)
    elif option == "6":
        change_password(client, address)


def check_user(user):
    f = open("clients.txt", "r")
    for line in f:
        line = line.strip("\n")
        separated_info = line.split(',')
        if separated_info[0] == user[0] and separated_info[1] == user[1]:
            f.close()
            return True
    f.close()
    return False


def list_messages_client(client, address, read):
    try:
        request = client.recv(1024)
    except KeyboardInterrupt:
        sys.exit(1)
        client.close()
    counter = 1
    messages = ""
    username = request.decode("utf-8")
    f = open("messages.txt", "r")
    for line in f:
        line = line.strip("\n")
        separated_info = line.split('|')
        if read == 0 and separated_info[2] == username and separated_info[3] == "0":
            messages += separated_info[0] + " send you:\n" + separated_info[1] + "\n"
        if read == 1 and separated_info[2] == username and separated_info[3] == "1":
            messages += separated_info[0] + " send you:\n" + separated_info[1] + "\n"
        if read == 2 and separated_info[2] == username:
            messages += str(counter) + "-" + separated_info[0] + " send you:\n" + separated_info[1] + "\n"
        counter += 1
    if messages != "":
        client.send(messages.encode("utf-8"))
    else:
        client.send("0".encode("utf-8"))
    return username
    f.close()


def mark_messages_read(client, address, username):
    f = open("messages.txt", "r")
    lines = ""
    for line in f:
        line = line.strip("\n")
        separated_info = line.split('|')
        if separated_info[2] == username:
            line_read = line[:-1]
            line_read = line_read + "1" + "\n"
            lines += line_read
        else:
            line = line + "\n"
            lines += line
    f.close()
    f = open("messages.txt", "w")
    f.write(lines)
    f.close()


def list_clients():
    users = ""
    f = open("clients.txt", "r")
    for line in f:
        line = line.strip("\n")
        separated_info = line.split(',')
        users += separated_info[0] + "\n"
    f.close()
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
    f = open("clients.txt", "r")
    for line in f:
        line = line.strip("\n")
        separated_info = line.split(',')
        if separated_info[0] == username:
            f.close()
            return True
    f.close()
    return False


def write_message(message):
    f = open("messages.txt", "a")
    f.write(message[0] + "|" + message[1] + "|" + message[2] + "|" + "0" +"\n")
    f.close()


def delete_message(client, address):
    username = list_messages_client(client, address, 2)
    try:
        request = client.recv(1024)
    except KeyboardInterrupt:
        sys.exit(1)
        client.close()
    message = int(request.decode("utf-8"))
    f = open("messages.txt", "r")
    counter = 0
    counter_array = []
    lines = ""
    for line in f:
        counter += 1
        counter_array.append(counter)
        line = line.strip("\n")
        separated_info = line.split('|')
        if message != counter:
            lines += line + "\n"
        else:
            if separated_info[2] != username:
                client.send("0".encode("utf-8"))
                return
    f.close()
    f = open("messages.txt", "w")
    f.write(lines)
    f.close()
    if message not in counter_array:
        client.send("-1".encode("utf-8"))
        return
    client.send("1".encode("utf-8"))


def change_password(client, address):
    try:
        request = client.recv(1024)
    except KeyboardInterrupt:
        sys.exit(1)
        client.close()
    user = request.decode("utf-8")
    user = json.loads(user)
    username = user[0]
    new_password = user[1]
    print new_password
    lines = ""
    f = open("clients.txt", "r")
    for line in f:
        line = line.strip("\n")
        separated_info = line.split(',')
        if separated_info[0] == username:
            lines += separated_info[0] + "," + new_password + "\n"
        else:
            lines += line + "\n"
    f.close()
    f = open("clients.txt", "w")
    f.write(lines)
    f.close()


def main():
    print "Hello World"
    server(9000)


if __name__ == '__main__':
    main()
