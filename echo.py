import socket
import thread

closed = False

def listenSock(connection):
    while closed == False: #change to bool which can be changed later
        received = connection.recv(1024)
        print "\n\n***\nReceived:\n" + received + "\n***\n\nCOMMAND (CHAT, JOIN, LEAVE, DISCONNECT): "

#setup message
def joinMessage(chatRoom, username):
    join_message = "JOIN_CHATROOM: " + str(chatRoom)
    ip_message = "CLIENT_IP: 0"
    port_message = "PORT: 0"
    user_name_message = "CLIENT_NAME: " + str(username)
    setupMessage = join_message + "\n" + ip_message + "\n" + port_message + "\n" + user_name_message
    return setupMessage

#leave message
def leaveMessage(chatRoom, join_id, username):
    room_num = "LEAVE_CHATROOM: " + chatRoom + "\n"
    unique_id = "JOIN_ID: " + join_id + "\n"
    client_name = "CLIENT_NAME: " + username
    
    return room_num + unique_id + client_name
 
def chatMessage(chatRoomID, join_id, username, msg):
    room_id = "CHAT: " + str(chatRoomID) + "\n"
    join_id = "JOIN_ID: " + str(join_id) + "\n"
    user = "CLIENT_NAME: " + str(username) + "\n"
    message = "MESSAGE: " + msg + "\n\n"
    format_msg = room_id + join_id + user + message
    return format_msg
    
#setup socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)        # Create a TCP socket
host = "localhost"                                             # On local host this time
port = 8004                                                  # Correct Port Number Required
s.connect((host, port))

#start listening thread
thread.start_new_thread(listenSock, (s, ))

#setup user Details
username = raw_input("Enter Chat username:" )

#main loop
while closed == False:
    message = raw_input("Enter Command: ")
    
    if message == "LEAVE":
        chatroom = raw_input("Enter ChatRoom to leave: ")
        message = leaveMessage(chatroom, "110", username)
    elif message == "JOIN":
        #usr = raw_input("Enter username": )
        chatRoomID = raw_input("Enter CharoomID num (0,1): ")
        message = joinMessage(chatRoomID, username)
    elif message == "CHAT":
        chatRoom = raw_input("Send to chatroom(0, 1): ")
        msg = raw_input("Enter msg: ")
        message = chatMessage(chatRoom, "110", username, msg)
    elif message == "DISCONNECT":
        message += ":"
    
    s.send(message)
    
    if message == "DISCONNECT:":
        closed = True
        break

raw_input("Session Ended, press enter")
    
s.close
