import time
from socket import *

pings = 1   
count=30
#Send ping 10 times 
while pings < 11 and count >0:  

    count-=1

    #Create a UDP socket
    clientSocket = socket(AF_INET, SOCK_DGRAM)

    #Set a timeout value of 1 second
    clientSocket.settimeout(1)

    #Ping to server
    message = 'test'

    addr = ("127.0.0.1", 12010)

    #Send ping
    start = time.time()
    clientSocket.sendto(message, addr)

    #If data is received back from server, print 
    try:
        data, server = clientSocket.recvfrom(1024)
        end = time.time()
        elapsed = end - start
        print str(data) + " " + str(pings) + " "+ str(elapsed)        

    #If data is not received back from server, print it has timed out  
    except timeout:
        print 'REQUEST TIMED OUT'
        pings+=1


    pings = pings - 1

message = 'close'
clientSocket.sendto(message, addr)
