#TODO
#GUI
#Buffering

from socket import *
import vlc
import time
import sys,os

def showProgress(start, end):
	barLength = 10
	status = ""
	progress = float(start)/float(end)
	progresstoshow = float("{0:.1f}".format(progress))
	if progress < 0:
		progress = 0
		status = "Halt...\r\n"
	if progress >= 1:
		progress = 1
		# status = "Done...\r\n"  
	block = int(round(barLength*progress))      
	text = "\rPercent: [{0}] {1}% {2}".format( "#"*block + "-"*(barLength-block), progresstoshow*100, status)
	# time.sleep(1)
	sys.stdout.write(text)
	sys.stdout.flush()

def startSend(destinationSocket,filename):
	f = open (filename,"rb") 
	size = os.fstat(f.fileno()).st_size
	destinationSocket.send(str(size) + "\n")
	showProgress(0, size)
	count = 1	
	c = f.read(1024)
	showProgress(count*1024, size)

	print("Sending file . . .")
	while c:
		destinationSocket.send(c)			# Sends data to client	   
		c = f.read(1024)
		count+=1
		showProgress(count*1024, size)
	# destinationSocket.send("EOF")	
	print("Transfer complete")

def startReceive(destinationSocket,filename):
	f = open (filename,"wb")
	size=int(destinationSocket.recv(10).split("\n")[0])
	print "Size: ",size
	showProgress(0, size)
	# count = 1
	print "waiting for file . . ."
	fileContent=destinationSocket.recv(1024)
	# Receives data upto 1024 bytes and stores in variables msg
	showProgress(len(fileContent), size)
	partFile = ""
	waste = ""
	while len(fileContent)<size:
		# print partFile
		# print len(fileContent),type(size),len(fileContent)<size
		fileContent += partFile
		# count+=1
		showProgress(len(fileContent), size)

		buff = size-len(fileContent)
		if(buff > 1024):
			buff = 1024
		# print "BUFF: ",buff	
		partFile=destinationSocket.recv(buff) 
	if(len(fileContent) == size):
		print "RECEIVE MATCH"
	else:
		waste = fileContent[size:]
		fileContent = fileContent[:size]
		print waste
	f.write(fileContent)
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
	time.sleep(5)
	# p.play()

def msgParser( socketdir ):
	# while(True):
	print "checking socket"
	while True:
		try:
			msgs = socketdir.recv(100)
			msgs = msgs.split('\n')
			for msg in msgs:
				if not msg:
					continue
				print "recvd: ",msg
				if msg == "beginsync":
					print str(time.time())
					t = str(time.time()*100)
					socketdir.send(t)
				elif msg == "quit":
					exit()
				elif msg =="beginplay":				
					playMP3("final.mp3")
				else:
					pass
					# ayachaTime = float(socketdir.recv(13))*1000000000
					# print ayachaTime
					# if (ayachaTime<0)
					# while( int(time.time()) != int(msg) ):
						# time.sleep(0.1)
						# continue
		except KeyboardInterrupt:
			print "Quitting!!!"
			break
		# time.sleep(5)
def msgSender( socketdir ):
	try:
		print "sending beginplay"
		socketdir.send("beginsync\n")
		senderTime = time.time()
		ayachaTime = socketdir.recv(13)
		receivedtime = time.time()
		roundtime = receivedtime - senderTime
		# appuratheCurrentTime = roundtime/2 + ayachaTime

		# print "receiverTime", ayachaTime
		print "senderTime", senderTime
		# print "appuratheCurrentTime", appuratheCurrentTime
		print "roundtime/2", roundtime/2

		delay = roundtime/2 - 0.02

		print "delay", delay
		import math
		delay = abs(delay)
	except Exception as e:
		print e
	finally:
		# t = int(time.time()) + 10
		# socketdir.send(str(delay*100))
		# while( int(time.time()) != t ):
			# time.sleep(0.1)
			# continue
		socketdir.send("beginplay")
		time.sleep(delay)
		playMP3("test.mp3")
		time.sleep(4)
		print "sending quit"
		socketdir.send("quit\n")
