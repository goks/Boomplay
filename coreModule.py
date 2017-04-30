#TODO
#GUI
#Buffering

from socket import *
import vlc
import time
import sys,os

if sys.platform == "win32":
	# On Windows, the best timer is time.clock()
	default_timer = time.clock
else:
	# On most other platforms the best timer is time.time()
	default_timer = time.time

def showProgress(start, end, callback, type):
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
	# text = "\rPercent: [{0}] {1}% {2}".format( "#"*block + "-"*(barLength-block), progresstoshow*100, status)
	text = "Percent: [{0}] {1}% {2}".format( "#"*block + "-"*(barLength-block), progresstoshow*100, status)
	# time.sleep(1)
	# sys.stdout.write(text)
	# sys.stdout.flush()
	callback(text,type,2)

def startSend(destinationSocket,filename, callback):
	type='server'
	callback("opening "+filename+'.', type)
	f = open (filename,"rb") 
	size = os.fstat(f.fileno()).st_size
	# callback("size: "+str(size)+'.', type)
	callback("Begin send. . . ", type)
	destinationSocket.send(str(size) + "\n")
	callback(". . . ", type)
	showProgress(0, size, callback, type)
	count = 1	
	c = f.read(1024)
	showProgress(count*1024, size, callback, type)

	print("Sending file . . .")
	while c:
		destinationSocket.send(c)			# Sends data to client	   
		c = f.read(1024)
		count+=1
		showProgress(count*1024, size, callback, type)
	# destinationSocket.send("EOF")	
	callback("Transfer complete",type)

def startReceive(destinationSocket,filename, callback):
	type='client'
	callback("opening "+filename+'.', type)
	f = open (filename,"wb")
	size=int(destinationSocket.recv(10).split("\n")[0])
	# callback("size: "+str(size)+'.', type)
	callback("Waiting for file. . . ", type)
	callback('. . . ',type)
	showProgress(0, size, callback, type)
	# count = 1
	fileContent=destinationSocket.recv(1024)
	# Receives data upto 1024 bytes and stores in variables msg
	showProgress(len(fileContent), size,callback, type)
	partFile = ""
	waste = ""
	while len(fileContent)<size:
		# print partFile
		# print len(fileContent),type(size),len(fileContent)<size
		fileContent += partFile
		# count+=1
		showProgress(len(fileContent), size, callback, type)

		buff = size-len(fileContent)
		if(buff > 1024):
			buff = 1024
		# print "BUFF: ",buff	
		partFile=destinationSocket.recv(buff) 
	if(len(fileContent) == size):
		callback("File received matches send size.", type)
	else:
		waste = fileContent[size:]
		fileContent = fileContent[:size]
		callback("The extras received: "+ waste, type)
	f.write(fileContent)
	callback("Transfer complete", type)
	callback(filename + " created.", type)
	f.close()

def createSocket(host,port,callback):
	print "****Server RUN****"
	type = "server"
	s=socket(AF_INET, SOCK_STREAM)

	callback("Begin binding. . . ", type)
	try:
		s.bind((host,port))
	except:
		callback("Binding fail", type)
		return
	callback("Binding success", type)
				 
	callback("Listening for connections.. ", type, 1)
	s.listen(1) 
	q,addr=s.accept()
	callback("received connecion from " + str(addr[0]) + " at " + str(addr[1]), type)
	return s,q


def closeSocket(socketdir):
	socketdir.close()

def createSocketStream(host, port):
	print "****Client RUN****"
	s=socket(AF_INET, SOCK_STREAM)
	s.connect((host,port)) 
	return s

def playMP3(filedes, callback, type):
	callback("Playing " + filedes, type)
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
	time.sleep(15)
	# p.play()

def msgParser( socketdir , callback):
	# while(True):
	type = "client"
	callback( "checking socket", type)
	while True:
		try:
			msgs = socketdir.recv(100)
			msgs = msgs.split('\n')
			for msg in msgs:
				if not msg:
					continue
				callback( "recvd: " + msg, type)
				if msg == "beginsync":
					print str(default_timer())
					t = str(default_timer()*100)
					socketdir.send(t)
				elif msg == "quit":
					sys.exit()
				elif msg =="beginplay":				
					playMP3("final.mp3", callback, type)
				else:
					pass
					# ayachaTime = float(socketdir.recv(13))*1000000000
					# print ayachaTime
					# if (ayachaTime<0)
					# while( int(time.default_timer()) != int(msg) ):
						# time.sleep(0.1)
						# continue
		except KeyboardInterrupt:
			callback( "Quitting!!!",type)
			break
		# time.sleep(5)
def msgSender( socketdir ,callback):
	type='server'
	try:
		callback("sending beginplay", type)
		socketdir.send("beginsync\n")
		senderTime = default_timer()
		ayachaTime = socketdir.recv(13)
		receivedtime = default_timer()
		roundtime = receivedtime - senderTime
		# appuratheCurrentTime = roundtime/2 + ayachaTime

		# print "receiverTime", ayachaTime
		callback("senderTime: " + str(senderTime),type)
		# print "appuratheCurrentTime", appuratheCurrentTime
		callback("roundtime/2: " + str(roundtime/2),type)

		delay = roundtime/2 - 0.02

		callback( "delay: " + str(delay), type)
		import math
		delay = abs(delay)
	except Exception as e:
		print e
		callback(e,type) 
	finally:
		# t = int(time.default_timer()) + 10
		# socketdir.send(str(delay*100))
		# while( int(time.default_timer()) != t ):
			# time.sleep(0.1)
			# continue
		socketdir.send("beginplay")
		time.sleep(delay)
		playMP3("test.mp3", callback, type)
		time.sleep(4)
		callback("sending quit", type)
		socketdir.send("quit\n")
