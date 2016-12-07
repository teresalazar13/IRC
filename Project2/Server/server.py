import socket
import sys
import json
import thread
import getopt
import hashlib


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
        request = client.recv(1024)
        option = request.decode("utf-8")
        if option == "9":
            print "Client with address", address, "closed connection"
            client.close()
            return
        process_client_request(client, address, option)


def process_client_request(client, address, option):
    if option == "0":
        register(client, address)
    elif option == "1":
        check_user(client, address)
    elif option == "2":
        username = list_messages_client(client, address, 0)
        mark_messages_read(client, address, username)
    elif option == "3":
        client.send(list_clients().encode("utf-8"))
    elif option == "4":
        send_message(client, address)
    elif option == "5":
        username = list_messages_client(client, address, 1)
    elif option == "6":
        delete_message(client, address)
    elif option == "7":
        change_password(client, address)
    elif option == "8":
        process_superuser(client, address)


def register(client, address):
    request = client.recv(1024)
    user = request.decode("utf-8")
    user = json.loads(user)
    user_pass = hashlib.sha1()
    user_pass.update(user[1])
    f = open("clients.txt", "a")
    f.write(user[0])
    f.write(",")
    f.write(user_pass.digest())
    f.write("\n")
    f.close()


def check_user(client, address):
    request = client.recv(1024)
    user = request.decode("utf-8")
    user = json.loads(user)
    f = open("clients.txt", "r")
    for line in f:
        line = line.strip("\n")
        separated_info = line.split(',')
        password = hashlib.sha1()
        password.update(user[1])
        password = password.digest()
        if separated_info[0] == user[0] and separated_info[1] == password:
            f.close()
            client.send("1".encode("utf-8"))
            return
    f.close()
    client.send("0".encode("utf-8"))


def check_superuser(user):
    f = open("superuser.txt", "r")
    text = f.read()
    text = text.strip("\n")
    text = text.split(",")
    password = hashlib.sha1()
    password.update(user[1])
    password = password.digest()
    f.close()
    if user[0] == text[0] and password == text[1]:
        return True
    else:
        return False


def list_messages_client(client, address, read):
    request = client.recv(1024)
    counter = 1
    messages = ""
    username = request.decode("utf-8")
    f = open("messages.txt", "r")
    for line in f:
        line = line.strip("\n")
        separated_info = line.split('|')
        if read == 0 and separated_info[2] == username and separated_info[3] == "0":
            messages += separated_info[0] + " sent you:\n" + separated_info[1] + "\n"
        if read == 1 and separated_info[2] == username and separated_info[3] == "1":
            messages += separated_info[0] + " sent you:\n" + separated_info[1] + "\n"
        if read == 2 and separated_info[2] == username:
            messages += str(counter) + "-" + separated_info[0] + " sent you:\n" + separated_info[1] + "\n"
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
    request = client.recv(1024)
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
    request = client.recv(1024)
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
    request = client.recv(1024)
    user = request.decode("utf-8")
    user = json.loads(user)
    username = user[0]
    new_password = hashlib.sha1()
    new_password.update(user[1])
    new_password = new_password.digest()
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


def process_superuser(client, address):
    superuser = client.recv(1024)
    superuser = json.loads(superuser)
    if check_superuser(superuser):
        print "Client entered superuser mode"
        client.send("1".encode("utf-8"))
    else:
        client.send("0".encode("utf-8"))
        request = client.recv(1024).decode("utf-8")
        if request == "1":
            superuser_pass = client.recv(1024).decode("utf-8")
            if superuser_pass == "1234":
                client.send("1".encode("utf-8"))
                f = open("superuser.txt", "w")
                f.write(superuser[0])
                f.write(",")
                user_pass = hashlib.sha1()
                user_pass.update(superuser[1])
                f.write(user_pass.digest())
                f.close()
            else:
                client.send("0".encode("utf-8"))
                return
        if request == "0":
            return
    while True:
        request = client.recv(1024)
        option = request.decode("utf-8")
        if option == "1":
            request = client.recv(1024)
            client_to_remove = request.decode("utf-8")
            delete_client(client_to_remove)
        elif option == "2":
            superuser_deletes_message(client, address)
        elif option == "3":
            print "Superuser quit superuser mode"
            return


def delete_client(client_to_remove):
    text = ""
    f = open("clients.txt", "r")
    for line in f:
        raw_line = line
        line = line.strip("\n")
        line = line.split(",")
        if line[0] != client_to_remove:
            text += raw_line
    f.close()
    f = open("clients.txt", "w")
    f.write(text)
    f.close()


def superuser_deletes_message(client, address):
    check = 0;
    messages = ""
    f = open("messages.txt", "r")
    counter = 0
    for line in f:
        counter += 1
        line = line.strip("\n")
        separated_info = line.split('|')
        messages += str(counter) + "-" + separated_info[0] + " sent:\n" + separated_info[1] + "\n"
    f.close()
    client.send(messages.encode("utf-8"))
    request = client.recv(1024)
    option = request.decode("utf-8")
    lines = ""
    f = open("messages.txt", "r")
    counter = 0
    for line in f:
        counter += 1
        if str(counter) != option:
            lines += line
        else:
            check = 1
    f.close()
    f = open("messages.txt", "w")
    f.write(lines)
    f.close()
    if check:
        client.send("1".encode("utf-8"))
    else:
        client.send("0".encode("utf-8"))


def main(argv):
    print "Hello World"
    port = ''
    try:
        opts, args = getopt.getopt(argv, "hp:", ["pport="])
    except getopt.GetoptError:
        print 'server.py -p <port>'
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print 'server.py -p <port>'
            sys.exit()
        elif opt in ("-p", "--pport"):
            port = arg
    if port != "":
        server(int(port))
    else:
        print 'ERROR - Usage: server.py -p <port>'
        return


if __name__ == '__main__':
    main(sys.argv[1:])
