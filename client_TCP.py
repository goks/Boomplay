# BOOmPlaY Server Code
import coreModule as core 
import time


 
class clientTcp():
	connected = False
	callback = None
	clientSocket = ""
	delay = 0
	type = 'client'


	"""docstring for clientTcp"""
	def __init__(self, callback):
		self.callback = callback		
		


	def beginConnection(self, HOST, PORT):
		self.clientSocket = core.createSocketStream(HOST, PORT)
		if self.clientSocket:
			self.callback("Connection successfull.", 'Client')
			self.connected=True
			self.callback("Mediaplayer switch activated.",self.type,3 )
		self.delay = core.calculateDelay( self.clientSocket,self.callback, self.type )	
		# core.startReceive(clientSocket, "final.mp3", callback)
		core.recvFromServer( self.clientSocket, self.callback)
		# core.closeSocket(clientSocket)

	def closeSocket(self):	
		core.closeSocket( self.serverSocket )

	def clientSendPause(self,timestamp):
		core.sendPause(self.clientSocket,timestamp,self.callback, self.type)

	def clientSendPlay(self):
		core.sendPlay(self.clientSocket,self.callback, self.type)

	def waitForDelay(self):
		time.sleep(self.delay)	

# main()	