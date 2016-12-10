import socket
import sys
import json
import getopt
import getpass
import signal

conn_to_server = []

def client(server_port):
	conn = create_socket(server_port)
	print 'Client connected'
	signal.signal(signal.SIGINT, ctrl_c_handler)

	### USED FOR shutdown_client
	conn_to_server.append(conn)

	user = []
	while True:
		option = menu(conn, user)
		#REGISTER
		if option == '0':
			conn.send(option.encode("utf-8"))
			response = register(conn)
			if response != -1:
				user = response
		#LOGIN
		elif option == '1':
			conn.send(option.encode('utf-8'))
			response = login(conn)
			if response != -1:
				user = response
		#LIST AUTHORIZED CLIENTS
		elif option == '3':
			conn.send(option.encode("utf-8"))
			print 'LIST OF AUTHORIZED CLIENTS'
			response = conn.recv(1024).decode('utf-8')
			print response
		#QUIT
		elif option == '9':
			shutdown_client()
		#IF NOT LOGGED IN
		elif option in ['2', '4', '5', '6', '7', '8'] and (user == [] or user == None):
			print 'Please login first'
			conn.send("Not logged in".encode('utf-8'))
		#IF LOGGED IN
		else:
			conn.send(option.encode('utf-8'))
			#LIST UNREAD MESSAGES
			if option == '2':
				list_messages(conn, user, 0)
			#SEND MESSAGE TO CLIENT
			elif option == '4':
				send_message(conn, user)
			#LIST READ MESSAGES
			elif option == '5':
				list_messages(conn, user, 1)
			#DELETE MESSAGES
			elif option == '6':
				delete_message(conn, user)
			#CHANGE PASSWORD
			elif option == '7':
				change_password(conn, user)
			#SUPERUSER
			elif option == '8':
				enter_superuser_mode(conn, user)
			else:
				print 'Invalid option'


def ctrl_c_handler(signum, frame):
	shutdown_client()

def shutdown_client():
	conn_to_server[0].send("9".encode('utf-8'))
	conn_to_server[0].close()
	sys.exit('Client disconnected')


#Create, connect and bind socket
#TESTED
def create_socket(port):
	try:
		client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	except socket.error as e:
		print(e)
		sys.exit('Error creating socket')
	host = socket.gethostname()
	try:
		client_socket.connect((host, port))
	except socket.error as e:
		print(e)
		sys.exit('Error connecting to server')
	print("Socket created successfully")
	return client_socket


#Main menu
def menu(conn, user):
	if user != [] and user != None:
		notifications = conn.recv(1024).decode("utf-8")
		if notifications != "0":
			print "You have a new message"
		else:
			print "No new notifications"
	else:
		print "Please log in to get notifications"

	option = raw_input("0 - Register\n"
				   "1 - Login\n"
				   "2 - List unread messages\n"
				   "3 - List authorized clients\n"
				   "4 - Send a message to a client\n"
				   "5 - List read messages\n"
				   "6 - Delete a message\n"
				   "7 - Change password\n"
				   "8 - Become superuser\n"
				   "9 - Quit\n"
				   "Option: ")
	return str(option)


#Menu for the superuser
def menu_superuser():
	option = raw_input("1 - Remove a client from database\n"
					   "2 - Remove a message\n"
					   "3 - Quit superuser mode\n"
					   "Option: ")
	return str(option)


#Register user in the server if not already logged in
def register(conn):
	username = ""
	while 0 == len(username) or len(username) >= 9:
		username = raw_input("Username (max length 9): ")
	password = getpass.getpass()
	user = [username, password]
	request = json.dumps(user)
	conn.send(request.encode("utf-8"))
	register_status = conn.recv(1024).decode("utf-8")
	if register_status == "Registered successfully":
		print "Register successfull. Welcome", username, "!"
		return user
	elif register_status == "Already Register":
		print "Already registered. Please login"
		return -1


#Login user into the server
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
	elif check_user == "0":
		print "Username or password incorrect"
		return -1
	else:
		print "User does not exist please register"


#Print read messages and unread messages depending on variable read
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


#Send email
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


#Delete message from the system
def delete_message(conn, user):
	if list_messages(conn, user, 2) == False or user == []:
		conn.send("-1".encode("utf-8"))
		return
	message_number = raw_input("Which message do you want do delete? Please select a number: ")
	conn.send(str(message_number).encode("utf-8"))
	check = conn.recv(1024).decode("utf-8")
	if check == "1":
		print "Message deleted successfully"
	elif check == "-1":
		print "Invalid input."


#Change Password
def change_password(conn, user):
	new_password = getpass.getpass()
	user = [user[0], new_password]
	user = json.dumps(user)
	conn.send(user.encode("utf-8"))
	print "Password was changed successfully"

#Enter superuser mode
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


#Deletes message as superuser
def superuser_deletes_message(conn, user):
	all_messages = conn.recv(1024).decode("utf-8")
	print all_messages
	if all_messages == "No messages":
		return
	message = raw_input("Which message do you want to delete: ")
	conn.send(str(message).encode("utf-8"))
	check = conn.recv(1024).decode("utf-8")
	if check == "1":
		print "Message was deleted successfully"
	else:
		print "Could not delete the message"


#Main function
def main(argv):
	signal.signal(signal.SIGINT, signal.SIG_IGN)
	port = ''
	try:
		opts, args = getopt.getopt(argv, "hp:")
	except getopt.GetoptError:
		sys.exit('python client.py -p <port>')
	for opt, arg in opts:
		if opt == '-h':
			sys.exit('python client.py -p <port>')
		elif opt == "-p":
			try:
				int(arg)
			except ValueError:
				sys.exit('python client.py -p <port>\nport has to be a number')
			if int(arg) < 1024:
				sys.exit('python client.py -p <port>\nport has to be bigger than 1023')
			port = arg
			client(int(port))
			return


if __name__ == '__main__':
	main(sys.argv[1:])
