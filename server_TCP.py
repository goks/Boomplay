# BOOmY Server Code
from socket import * 
import coreModule as core 
 
HOST="127.0.0.1"               
PORT=4446             
 




def main():
    serverSocket,clientSocket = core.createSocket(HOST, PORT)
    core.startSend(clientSocket, "test.mp3")
    # serverSocket,clientSocket = core.createSocket(HOST, PORT)
    core.msgSender( clientSocket )
    core.closeSocket( serverSocket )

main()  