import socket
import thread

closed = False

def listenSock(connection):
    while closed == False: #change to bool which can be changed later
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

#leave message
def leaveMessage(chatRoom, join_id, username):
    room_num = "LEAVE_CHATROOM: " + chatRoom + "\n"
    unique_id = "JOIN_ID: " + join_id + "\n"
    client_name = "CLIENT_NAME: " + username
    
    return room_num + unique_id + client_name
    
s.send(setupMessage)

#main
while closed == False:
    message = raw_input("Enter Chat: ")
    
    if message == "LEAVE":
        chatroom = raw_input("Enter ChatRoom to leave: ")
        message = leaveMessage(chatroom, "110", "FERDIA")
    
    s.send(message)
    
    if message == "DISCONNECT:":
        closed = True
        break

raw_input("Ready to quit?: ")
    
s.close
