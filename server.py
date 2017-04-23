import random
from socket import *

	# Create a UDP socket
	# Notice the use of SOCK_DGRAM for UDP packets
serverSocket = socket(AF_INET, SOCK_DGRAM)

# Assign IP address and port number to socket
serverSocket.bind(('127.0.0.1', 12010))
print(" BIND OK")

while True:
    # Generate random number in the range of 0 to 10
    rand = random.randint(0, 10)

    # Receive the client packet along with the address it is coming from
    message, address = serverSocket.recvfrom(1024)

    # Capitalize the message from the client
    message = message.upper()

    print "\"" + message + "\""

    # If rand is less is than 4, we consider the packet lost and do notrespond
    if rand < 4:
        continue

    # Otherwise, the server responds
    serverSocket.sendto(message, address) 

    if(message=="CLOSE"):
        print("Quitting")
        serverSocket.close()
        exit()

