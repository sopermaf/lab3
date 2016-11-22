import socket

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)        # Create a TCP socket
host = "localhost"	    # On local host this time
port = 8004  # Correct Port Number Required

aim_message = "ferdia"
message = "hello"

#user details
username = "FERDIA"

#the messages required for joining a chat room
join_message = "JOIN_CHATROOM: 0"
ip_message = "CLIENT_IP: 0"
port_message = "PORT: 0"
user_name_message = "CLIENT_NAME: " + username

setupMessage = join_message + "\n" + ip_message + "\n" + port_message + "\n" + user_name_message

s.connect((host, port))
s.send(setupMessage)

print s.recv(1024)

s.close


#2 threads, one recieve and one send
#recieve to listen for broadcasts or response
