import socket
import threading
import os

#shared data setup
connections = []
client_addr = []
connectLock = threading.Condition()

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
            newClient(copy_connect, copy_addr, self.threadID)
        

def newClient(connection, client_address, threadID):
    print 'connection from: ' + str(client_address) + " -- processing on thread " + str(threadID)
    inData = connection.recv(256)
    print 'received: ' + str(inData)
    connection.sendall(inData)
    print 'sending back: ' + str(inData)
    print 'closing connection\n'
    connection.close()

def parseMessage(message):
	print "do something"
	
	return -1
	
#create the threads
threads = []
NUM_THREADS = 10
for i in range(0, NUM_THREADS):
	thread_name = "Thread-" + str(i)
	threads.append(myThread(i, thread_name, i))
	
#start the threads
for j in range(0, NUM_THREADS):
	threads[j].start()

#create TCP socket
PORT = 8004

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind(('localhost', PORT))
sock.listen(1)

while True:
    # Wait for a connection
    print 'waiting for a connection'
    new_connect, new_addr = sock.accept()
    
    with connectLock:
    	#append new collection to the end
    	connections.append(new_connect)
    	client_addr.append(new_addr)
    	#notify a thread
    	connectLock.notify()
    
     
    
