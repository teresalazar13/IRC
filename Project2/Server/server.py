import socket
import sys
import json
from threading import Thread
import getopt
import hashlib
import signal

#Threadpool
threads = []
#Thread exiting control variable
exitThreads = 0
#Max users that can connect to the server
max_users = 5

#Create, bind and listen to socket
def create_socket(port):
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	host = socket.gethostname()
	s.bind((host, port))
	s.listen(max_users)
	print "Socket creation successfull"
	return s


#Ctrl c handler
def ctrl_c_handler(signum, frame):
	shutdown_server()

#Shutdown server
def shutdown_server():
	join_threads()
	sys.exit('Server terminating')


#Join threads
def join_threads():
	exitThreads=1
	for thread in threads:
		thread.join

#Main setup and runtime of the server
def server(port):
	server_socket = create_socket(port)
	print "The server is ready to receive"
	signal.signal(signal.SIGINT, ctrl_c_handler)
	while True:
		client, address = server_socket.accept()
		t = Thread(target=process_client,  args=(client, address))
		t.daemon = True;
		t.start()
		threads.append(t)


#Thread to handle client requests
def process_client(client, address):
	user = []
	while True:
		if user != [] and user != None:
			check_notifications(client, address, user)
		option = client.recv(1024).decode("utf-8")
		if option == "9":
			print "Client with address", address, "closed connection"
			client.close()
			return
		if option == "Not logged in":
			continue
		process_client_request(client, address, option, user)
		if exitThreads == 1:
			return


#Handle requested action from the client
#TEST
def process_client_request(client, address, option, user):
	#TESTED
	if option == "0":
		test = register(client, address)
		if test == -1:
			return
		else:
			user.append(test[0])
			user.append(test[1])
	#TESTED
	elif option == "1":
		response = check_user(client, address)
		if response != -1:
			user.append(response[0])
			user.append(response[1])
	#TESTED
	elif option == "2":
		username = list_messages_client(client, address, 0)
		mark_messages_read(client, address, username)
	#TESTED
	elif option == "3":
		response = list_clients()
		client.send(response.encode("utf-8"))
	#TESTED
	elif option == "4":
		send_message(client, address)
	#TEST
	elif option == "5":
		username = list_messages_client(client, address, 1)
	elif option == "6":
		delete_message(client, address)
	elif option == "7":
		change_password(client, address)
	elif option == "8":
		process_superuser(client, address)

#Register client in the server
#TESTED
def register(client, address):
	user = client.recv(1024).decode("utf-8")
	user = json.loads(user)

	registered_users = []
	f = open("clients.txt", "r")
	for line in f:
		registered_users.append(line.split(", ")[0])
	f.close()

	if user[0] in registered_users:
		client.send("Already Register".encode("utf-8"))
		return -1
	else:
		f = open("clients.txt", "a")
		f.write(user[0])
		f.write(", ")
		f.write(encode(user[1]))
		f.write("\n")
		f.close()
		client.send("Registered successfully".encode("utf-8"))
		return user

#Encodes string
#TESTED
def encode(str):
	return hashlib.sha1(str).hexdigest()

#Check if the user exist
#TESTED
def check_user(client, address):
	user = client.recv(1024).decode("utf-8")
	user = json.loads(user)
	f = open("clients.txt", "r")
	for line in f:
		line = line.strip("\n")
		separated_info = line.split(', ')
		password = encode(user[1])
		if separated_info[0] == user[0] and separated_info[1] == password:
			f.close()
			client.send("1".encode("utf-8"))
			return user
		if separated_info[0] == user[0] and separated_info[1] != password:
			f.close()
			client.send("0".encode("utf-8"))
			return -1
	f.close()
	client.send("2".encode("utf-8"))
	return -1


def check_superuser(user):
    f = open("superuser.txt", "r")
    text = f.read()
    text = text.strip("\n")
    text = text.split(",")
    password = encode(user[1])
    f.close()
    if user[0] == text[0] and password == text[1]:
        return True
    else:
        return False

#Get notifications of logged in client
#TESTED
def check_notifications(client, address, user):
	notifications = 0;
	lines = ""
	f = open("notify.txt", "r")
	for line in f:
		line = line.strip("\n")
		if line == user[0]:
			notifications += 1
		else:
			lines += line + "\n"
	f.close()
	f = open("notify.txt", "w")
	f.write(lines)
	f.close()
	client.send(str(notifications).encode("utf-8"))


#Return messages for the client, read and unread depending on the read variable
#TESTED
def list_messages_client(client, address, read):
    counter = 1
    messages = ""
    username = client.recv(1024).decode("utf-8")
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


#Mark message as read
#TESTED
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

#List clients registered in the server
#TESTED
def list_clients():
	registered_users = []
	f = open("clients.txt", "r")
	for line in f:
		if line == "\n":
			continue
		separated_info = line.split(', ')
		registered_users.append(separated_info[0])
	f.close()
	registered_users = '\n'.join(registered_users)
	return registered_users


#Send message to a user
#TESTED
def send_message(client, address):
    message = client.recv(1024).decode("utf-8")
    message = json.loads(message)
    if check_username(message[2]):
        client.send("1".encode("utf-8"))
        write_message(message)
    else:
        client.send("0".encode("utf-8"))
        return
    f = open("notify.txt", "a")
    f.write(message[2])
    f.write("\n")
    f.close()


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
    message = int(client.recv(1024).decode("utf-8"))
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
    user = client.recv(1024).decode("utf-8")
    user = json.loads(user)
    username = user[0]
    new_password = encode(user[1])
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
    superuser = client.recv(1024).decode("utf-8")
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
                f.write(encode(superuser[1]))
                f.close()
            else:
                client.send("0".encode("utf-8"))
                return
        if request == "0":
            return
    while True:
        option = client.recv(1024).decode("utf-8")
        if option == "1":
            client_to_remove = client.recv(1024).decode("utf-8")
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
    option = client.recv(1024).decode("utf-8")
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
	signal.signal(signal.SIGINT, signal.SIG_IGN)
	print "Welcome to our simple email server"
	port = ''
	try:
		opts, args = getopt.getopt(argv, "hp:")
	except getopt.GetoptError:
		sys.exit('python server.py -p <port>')
	for opt, arg in opts:
		if opt == '-h':
			sys.exit('python server.py -p <port>')
		elif opt == "-p":
			try:
				int(arg)
			except ValueError:
				sys.exit('python server.py -p <port>\nport has to be a number')
			if int(arg) < 1024:
				sys.exit('python server.py -p <port>\nport has to be bigger than 1023')
			port = arg
			server(int(port))
			return


if __name__ == '__main__':
	main(sys.argv[1:])
