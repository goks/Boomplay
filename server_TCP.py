# BOOmPlaY Server Code
from socket import * 
import coreModule as core 
 
HOST="192.168.1.101"               
PORT=4446             
 




def main():
    serverSocket,clientSocket = core.createSocket(HOST, PORT)
    core.startSend(clientSocket, "test.mp3")
    # serverSocket,clientSocket = core.createSocket(HOST, PORT)
    core.msgSender( clientSocket )
    core.closeSocket( serverSocket )

main()  