# BOOmPlaY Server Code
from socket import * 
import coreModule as core 
 
def beginConnection(HOST, PORT,callback):
    serverSocket,clientSocket = core.createSocket(HOST, PORT, callback)
    core.startSend(clientSocket, "test.mp3", callback)
    # serverSocket,clientSocket = core.createSocket(HOST, PORT)
    core.msgSender( clientSocket,callback )
    core.closeSocket( serverSocket )
