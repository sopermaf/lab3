import socket

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)        # Create a TCP socket
host = "localhost"	    # On local host this time
port = 8004  # Correct Port Number Required

aim_message = "ferdia"
message = "hello"

s.connect((host, port))
s.send(message)

print s.recv(256)
s.close
