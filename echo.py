import socket
import thread

def listenSock(connection):
    while True: #change to bool which can be changed later
        print "\n\nReceived:"
        print connection.recv(1024)
        print "\nEnter Chat: "
        
#user details
username = "FERDIA"

#setup socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)        # Create a TCP socket
host = "localhost"	                                         # On local host this time
port = 8004                                                  # Correct Port Number Required
s.connect((host, port))

#start listening thread
thread.start_new_thread(listenSock, (s, ))

#setup message
join_message = "JOIN_CHATROOM: 0"
ip_message = "CLIENT_IP: 0"
port_message = "PORT: 0"
user_name_message = "CLIENT_NAME: " + username
setupMessage = join_message + "\n" + ip_message + "\n" + port_message + "\n" + user_name_message

s.send(setupMessage)

#main
while True:
    message = raw_input("Enter Chat: ")
    s.send(message)


s.close
