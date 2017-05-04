#TODO
#GUI
#Buffering

from socket import *
import vlc
import time
import struct
import sys,os

if sys.platform == "win32":
	# On Windows, the best timer is time.clock()
	default_timer = time.clock
else:
	# On most other platforms the best timer is time.time()
	default_timer = time.time

# ******************* PROGRESS BAR FUMCTION ******************

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

# ******************* SOCKET OPEN AND CLOSE ******************
	
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

# ******************* MP3 CONTROLS MUSICPLAYER ******************
def playMP3(filedes, callback, type):
	callback("Playing " + filedes, type)
	player = vlc.MediaPlayer()
	player.set_mrl(filedes)
	player.play()
	# time.sleep(15)
	# callback("software volume: "+ str(player.audio_get_volume), type)
	#Reduce the volume to 70%
	# player.audio_set_volume(100)
	return player

def pauseMP3(timestamp,player, callback, type):
	callback("Pausing", type)
	player.pause()
	callback("setting offset", type)
	player.set_time(int(timestamp))
	callback("offset set", type)

def stopMP3(player, callback, type):
	player.stop()
	callback('. . . ',type)
	callback("playback stopped", type)	
	callback('. . . ',type)


# ************************ IMPORTANT ************************
# ********** MSG SEND AND RECEIVE CORE FUNCTIONS ************
def recv_msg(sock):
    # Read message length and unpack it into an integer
    raw_msglen = recvall(sock, 4)
    if not raw_msglen:
        return None
    msglen = struct.unpack('>I', raw_msglen)[0] 
    # Read the message data
    return recvall(sock, msglen)

def recvall(sock, n):
    # Helper function to recv n bytes or return None if EOF is hit
    data = ''
    while len(data) < n:
        packet = sock.recv(n - len(data))
        if not packet:
            return None
        data += packet
    return data

def send_msg(sock, msg):
    # Prefix each message with a 4-byte length (network byte order)
    # pack to bigindian
    msg = struct.pack('>I', len(msg)) + msg
    sock.sendall(msg)

# ************************ FILE IO ************************

def write_file(filename, file):
	f = open(filename, 'wb')
	f.write(file) 
	f.close()   

# def read_file(filename):
# 	f = open(filename, 'rb')



# ******************** CLIENT/SERVER LISTENER ********************
def recvFromServer( socketdir , callback, type = "client"):
	# while(True):
	filename = ''
	callback( "checking socket", type)
	check = True
	player = None

	while True:
		try:
			msg = recv_msg( socketdir )
			# Initial check
			if not msg:
				callback("server blocking ",  type)
				# time.sleep(1)
				continue
			try:	
				callback( "recvd: \'" +msg+ "'", type)
			except:
				callback( "received unknown", type)
				continue

			# switch..case begins	
			if msg == "beginsync":
				print str(default_timer())
				t = str(default_timer()*100)
				# socketdir.send(t)
				send_msg(socketdir,t)

			elif msg == "receiveMp3":
				filename = recv_msg(socketdir)
				file = recv_msg(socketdir)
				callback(filename + " received.", type)
				callback("Transfer complete", type)
				write_file(filename,file)
				callback(filename +" created.", type)

			elif msg =="beginplay":	
				# show the filename in nowplaying
				player = playMP3(filename, callback, type)
				callback(filename,type,5)	
				callback(player,type,6)	


			elif msg =="pause":
				timestamp = recv_msg(socketdir)
				if(type=="server"):
					player = callback( "",type,7)
				pauseMP3(timestamp, player, callback, type)
				

			elif msg == 'play':
				if(type=="server"):
					player = callback( "",type,7)
					if not player.is_playing():
						player.play()

			elif msg == 'stop':
				if(type=="server"):
					player = callback( "",type,7)
				stopMP3(player, callback, type)

			elif msg == "quit":
				sys.exit()

			else:
				print "received msg: " + msg
				continue

		except KeyboardInterrupt:
			callback( "Quitting!!!",type)
			break
		except:
			# socket.error
			# if e.errno == errno.ECONNRESET:
			# 	callback( "Disconnected", type)
			# 	# Handle disconnection -- close & reopen socket etc.	
			# 	break
			# else:
				# raise	
			raise
# ******************** SERVER MSG SENDER ********************

def startSendMp3(destinationSocket,filename, callback):
	type='server'
	#STEP 1
	msg = "receiveMp3"
	callback(msg + ' sent', type)
	send_msg(destinationSocket,msg)
	#STEP 2
	filename_to_send = filename.split('/')[-1]
	print"server>>> "+ filename_to_send +','+ str(len(filename_to_send))
	callback("sending filename : "+filename_to_send, type)
	print("sending filename : "+filename_to_send)
	msg = filename_to_send
	callback(msg + ' sent', type)
	send_msg(destinationSocket,msg)
	#STEP 3
	callback("opening "+filename+'.', type)
	f = open (filename,"rb") 
	size = os.fstat(f.fileno()).st_size
	callback(". . . ", type)
	print("Sending file . . .")
	msg = f.read()	
	send_msg(destinationSocket,msg)
	callback("Transfer complete",type)

def sendBeginplay(destinationSocket, callback):
	type='server'
	msg = "beginplay"
	callback(msg + ' sent', type)
	send_msg(destinationSocket,msg)

def sendPause(destinationSocket, timestamp, callback, type='server'):
	#STEP 1
	msg = "pause"
	send_msg(destinationSocket,msg)
	callback(msg + ' sent', type)
	#STEP 2
	msg = timestamp
	send_msg(destinationSocket,msg)
	callback("timestamp sent", type)

def sendPlay(destinationSocket, callback, type='server'):
	msg = "play"
	send_msg(destinationSocket,msg)
	callback(msg + ' sent', type)

def sendStop(destinationSocket, callback, type='server'):
	msg = "stop"
	send_msg(destinationSocket,msg)
	callback(msg + ' sent', type)

# ******************** DELAY CALCULATOR ********************

def calculateDelay( socketdir ,callback,type='server'):
	# try:
	msg = "beginsync"
	send_msg(socketdir,msg)
	callback(msg + ' sent', type)

	senderTime = default_timer()
	# ayachaTime = socketdir.recv(13)
	ayachaTime = recv_msg(socketdir)
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
	# except Exception as e:
	# 	print e
	# 	callback(e,type)
	# 	return -1
	callback("sync completed", type)
	return delay
		# socketdir.send("beginplay")
		# time.sleep(delay)
		# playMP3("test.mp3", callback, type)
		# time.sleep(4)
		# callback("sending quit", type)
		# socketdir.send("quit\n")
