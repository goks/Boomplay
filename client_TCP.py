# BOOmPlaY Server Code

import coreModule as core 
 
# HOST="192.168.1.100"               
# PORT=4446
class clientTcp():
	connected = False
	callback = None
	clientSocket = ""
	"""docstring for clientTcp"""
	def __init__(self, callback):
		self.callback = callback		
		


	def beginConnection(self, HOST, PORT):
		self.clientSocket = core.createSocketStream(HOST, PORT)
		if self.clientSocket:
			self.callback("Connection successfull.", 'Client')
			self.connected=True
		# core.startReceive(clientSocket, "final.mp3", callback)
		core.recvFromServer( self.clientSocket, self.callback)
		# core.closeSocket(clientSocket)

	def closeSocket(self):	
		core.closeSocket( self.serverSocket )


# main()	