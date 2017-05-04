# BOOmPlaY Server Code
from socket import * 
import coreModule as core
from threading import Thread 
import time
 	
class serverTcp():
	connected = False
	serverSocket = None
	clientSocket = ""
	callback = False
	delay = 0
	player = '' # vlc player instance
	type = 'server'

	
	"""docstring for serverTcp"""
	def __init__(self,callbackF):
		self.callback=callbackF
		

	def beginConnection(self, HOST, PORT):
		self.serverSocket,self.clientSocket = core.createSocket(HOST, PORT, self.callback)
		if self.serverSocket and self.clientSocket:
			self.callback("MediaPlayer switch activated", self.type, 4)
			self.connected = True
			self.delay = core.calculateDelay( self.clientSocket,self.callback )
			self.startServerListener()
		# while True:
		# 	if self.connected:
		# 		try:
		# 			# self.startServerListener()
		# 			while True:
		# 				if (not self.connected):
		# 					print("running")
		# 					exit(1)										 #Exit on Keyboard Interrupt
		# 		except (KeyboardInterrupt, SystemExit):
		# 			stdout.flush()
		# 			print '\nConnection to server closed.'
		# 			#Close server
		# 		else:
		# 			raise					  
	def startServerListener(self):
		self.callback("Begin server listener", self.type)
		core.recvFromServer( self.clientSocket, self.callback, self.type)				
	def serverSendMp3(self,filename):
		core.startSendMp3(self.clientSocket, filename, self.callback)
		core.sendBeginplay(self.clientSocket, self.callback)
	def serverSendPlay(self):
		core.sendPlay(self.clientSocket,self.callback)
	def serverSendStop(self):
		core.sendStop(self.clientSocket,self.callback)	
	def serverSendPause(self,timestamp):
		core.sendPause(self.clientSocket,timestamp,self.callback)

	def waitForDelay(self):
		time.sleep(self.delay)



	def closeSocket(self):	
		core.closeSocket( self.serverSocket )
