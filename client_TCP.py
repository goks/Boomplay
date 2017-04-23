# BOOmPlaY Server Code

import coreModule as core 
 
HOST="192.168.1.101"               
PORT=4446

def main():
	clientSocket = core.createSocketStream(HOST, PORT)
	core.startReceive(clientSocket, "final.mp3")
	# clientSocket = core.createSocketStream(HOST, PORT)
	core.msgParser( clientSocket )
	core.closeSocket(clientSocket)
	# core.playMP3("final.mp3")

main()	