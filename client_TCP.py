# BOOmPlaY Server Code

import coreModule as core 
 
# HOST="192.168.1.100"               
# PORT=4446


def beginConnection(HOST, PORT,callback):
	clientSocket = core.createSocketStream(HOST, PORT)
	if clientSocket:
		callback("Connection successfull.", 'Client')
	# core.startReceive(clientSocket, "final.mp3", callback)
	core.msgParser( clientSocket, callback)
	# core.closeSocket(clientSocket)


# main()	