import socket
import threading
import os

#shared data setup
connections = []
client_addr = []
connectLock = threading.Condition()
uniqueNum_Lock = threading.Lock()

#chatroom arrays of sockets or maybe dictionarys??
chat1 = []
chat2 = []

#create TCP socket
PORT = 8004
IP_ADDR = 'localhost'

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind((IP_ADDR, PORT))
sock.listen(1)

class myThread (threading.Thread):
    def __init__(self, threadID, name, counter):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.counter = counter
        
    def run(self):
        print "Starting " + self.name        
        while True:
            #lock for concurrency
            with connectLock:
                while len(connections) < 1: #no connections to reply to
                    connectLock.wait()
                #copy the data to local version
                copy_connect = connections[0]
                copy_addr = client_addr[0]
                connections.pop(0)
                client_addr.pop(0)

            #lock not needed 
            newClient(copy_connect)
        
def newClient(connection):
    terminate = False    
    
    while terminate == False:
        inData = connection.recv(1024)
        print inData
        
        #***could go wrong if someone sent this in their message! workable but not safe!!***
        if "JOIN_CHATROOM:" in inData:
            joinChat(inData, connection)
            print "USER JOINED"
        elif "LEAVE_CHATROOM:" in inData:
            #call the leave function
            print "LEAVE"
        elif "CHAT:" in inData:
            #call the broadcast function
            print "CHAT MESSAGE"
        elif "DISCONNECT:" in inData:
            terminate = True
            print "USER DISCONNECTED"
        else:
            sendError(404, "NO PUEDO ENCONTRAR EL CODIGO", connection)
    
    connection.close()
    #check if still in chatrooms and remove?
    
def joinChat(inMess, connection):
    #get the username and chatRoom
    message = str(inMess).split('\n')
    CHAT_CHOICE = message[0].split(' ')[1]
    CLIENT_NAME = message[3].split(' ')[1]
    joined = False
    
    #change to accomadate any size int
    if CHAT_CHOICE == '0':
        chat1.append(connection)
        joined = True
    elif CHAT_CHOICE == '1':
        chat2.append(connection)
        joined = True
    
    #reply success and broadcast join message, OR error
    if joined == False:
        sendError(405, "JOIN UNSUCCESSFUL - UNKNOWN ROOM NUMBER", connection)
    else:
        #setup unique ID
        uniqueID = 101
        
        #contact client
        room_join = "JOINED_CHATROOM: " + str(CHAT_CHOICE) + "\n"
        serv_ip = "SERVER_IP: " + str(IP_ADDR) + "\n"
        port_num = "PORT: " + str(PORT) + "\n"
        room_id = "ROOM_REF: "  + "11" + str(CHAT_CHOICE) + "\n" #FANCY LOOKING UNIQUE ID
        join_id = "JOIN_ID: " + str(uniqueID)
        client_message = room_join + serv_ip + port_num + room_id + join_id
        connection.send(client_message)
        
        #contact chatroom
        chat_alert = "USER: " + CLIENT_NAME + " has joined the room"
        broadCast(chat_alert, CHAT_CHOICE, connection)
    
def broadCast(message, chatID, senderSock):
    #could be changed to not send Sender back their message??
    if chatID == "0":
        chatRoom = chat1
    elif chatID == "1":
        chatRoom = chat2
    else:
        print "BROADCAST chatroom select error"
    
    for user in chatRoom:
        user.send(message)

def leaveChat(inMess, connection):    
    print "leave chat func call"
    
def sendError(error_code, error_description, connection):
    #compose the error message
    code = "ERROR_CODE: " + str(error_code) + "\n"
    descript = "ERROR_DESCRIPTION: " + str(error_description) 
    message = code + descript
    
    #send the error
    connection.send(message)
    
#create the threads
threads = []
NUM_THREADS = 10
for i in range(0, NUM_THREADS):
    thread_name = "Thread-" + str(i)
    threads.append(myThread(i, thread_name, i))
    
#start the threads
for j in range(0, NUM_THREADS):
    threads[j].start()

# Wait for a connection
print 'ready for connections'

while True:
    new_connect, new_addr = sock.accept()
    
    with connectLock:
        #append new collection to the end
        connections.append(new_connect)
        client_addr.append(new_addr)
        
        #notify a thread
        connectLock.notify()