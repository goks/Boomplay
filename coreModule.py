from socket import *
import vlc
import time

def startSend(destinationSocket,filename):
	f = open (filename,"rb")
	c = f.read(1024)
	print("Sending file . . .")
	while c:
		destinationSocket.send(c)						# Sends data to client	   
		c = f.read(1024)
	destinationSocket.send("EOF")	
	print("Transfer complete")

def startReceive(destinationSocket,filename):
	f = open (filename,"wb")
	print "waiting for file . . ."
	partFile=destinationSocket.recv(1024)			# Receives data upto 1024 bytes and stores in variables msg
	while partFile != "EOF":
		# print partFile
		f.write(partFile)
		partFile=destinationSocket.recv(1024) 
	print("Transfer complete")		  
	print(filename + " created.")
	f.close()

def createSocket(host,port):
	print "****Server RUN****"
	s=socket(AF_INET, SOCK_STREAM)
	s.bind((host,port)) 
	print "Listening for connections.. "
	s.listen(1) 
	q,addr=s.accept()
	print "received connecion from " + str(addr[0]) + " at " + str(addr[1])
	return s,q


def closeSocket(socketdir):
	socketdir.close()

def createSocketStream(host, port):
	print "****Client RUN****"
	s=socket(AF_INET, SOCK_STREAM)
	s.connect((host,port)) 
	return s

def playMP3(filedes):
	print "Playing music"
	instance = vlc.Instance()
	player = instance.media_player_new()
	# if sys.platform == 'win32':
	#			 player.set_hwnd(self.window.handle)
	#		 else:
	#			 player.set_xwindow(self.window.xid)
	media = instance.media_new(filedes)
	player.set_media(media)
	# p = vlc.MediaPlayer(filedes)
		#set the player position to be 50% in
	player.set_position(50)

	#Reduce the volume to 70%
	player.audio_set_volume(100)
	player.play()
	time.sleep(10)
	# p.play()

def msgParser( socketdir ):
	# while(True):
	print "checking socket"
	while True:
		try:
			time.sleep(1)
			msg=socketdir.recv(100)
			if not msg:
				continue
			print "recvd: ",msg,"EOF"
			if msg == "beginplay\n":
				playMP3("final.mp3")
			if msg == "quit\n":
				exit()
		except KeyboardInterrupt:
			print "Quitting!!!"
			break
		# time.sleep(5)
def msgSender( socketdir ):
	try:
		print "sending beginplay"
		socketdir.send("beginplay\n")
	except Exception as e:
		print e
	finally:
		playMP3("test.mp3")
		time.sleep(4)
		print "sending quit"
		socketdir.send("quit\n")
