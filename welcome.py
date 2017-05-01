from kivy.app import App

from kivy.uix.widget import Widget
from kivy.uix.screenmanager import ScreenManager, Screen, SlideTransition
from kivy.uix.button import Button
from kivy.properties import ObjectProperty
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.popup import Popup
# from kivy.core.audio import SoundLoader

#local imports
import network_module as nm
import server_TCP as sm
import client_TCP as cm
import vlc

from os import listdir, path
from threading import Thread,Event

class tabbedScreen(Screen):
	"""docstring for tabbedScreen"""
	def __init__(self, **kwargs):
		# self.path = './dataset/train'
		super(tabbedScreen, self).__init__(**kwargs)
		callback_to_call = self.callback
		try:
			self.ids.serverIp.text = nm.get_local_ip()
		except:
			self.callback("Connect to a network :/", "server")

	def validate_ip_address( self, ip ):
		import socket
		try:
			socket.inet_pton(socket.AF_INET, ip)
		except AttributeError:  # no inet_pton here, sorry
			try:
				socket.inet_aton(ip)
			except socket.error:
				return False
			return ip.count('.') == 3
		except socket.error:  # not a valid ip
			return False

		return True

	def validate_port_address( self, port ):
		if port<65536 and port>0:
			return True
		else:
			return False	

	def callback( self, content, type, callcode=0 ):
		if(type == "server"):
			u = self.ids.serverMessageBox.text
			if (callcode==2):
				u = u.split('\n')[:-1]
				u = '\n'.join(u)
			self.ids.serverMessageBox.text = u + '\n' + content
		else:
			u = self.ids.clientMessageBox.text
			if (callcode==2):
				u = u.split('\n')[:-1]
				u = '\n'.join(u)
			self.ids.clientMessageBox.text = u + '\n' + content	
		if(callcode == 1):
			# server waiting for connections
			self.ids.serverConnectBtn.disabled = True
				

	def beginServerConn(self):
		callback_to_call = self.callback
		host = self.ids.serverIp.text

		try:
			port = int(self.ids.serverPort.text)
		except:
			self.callback("Check port :/", "server")
			return

		# self.callback( str(host) + str(port) + str(type(host)) + str(type(port)), "server")
		if not self.validate_ip_address( host ):
			self.callback( "Invalid IP address", "server")
			return
		if not self.validate_port_address( port ):
			self.callback( "Invalid port address", "server")
			return
		text = "Trying to bind to "+host+" at "+str(port)+"."
		self.callback(text , "server")
		# sm.beginConnection(host,port,callback_to_call)
		t = Thread( target = sm.beginConnection, args=(host,port,callback_to_call))
		t.daemon = True
		t.start()


	def beginClientConn(self):
		callback_to_call = self.callback
		host = str(self.ids.serverIp.text)

		try:
			port = int(self.ids.serverPort.text)
		except:
			self.callback("Check port :/", "client")
			return

		# self.callback( str(host) + str(port) + str(type(host)) + str(type(port)), "server")
		if not self.validate_ip_address( host ):
			self.callback( "Invalid IP address", "client")
			return
		if not self.validate_port_address( port ):
			self.callback( "Invalid port address", "client")
			return
		text = "Trying to connect to "+host+" at "+str(port)+"."
		self.callback(text , "client")
		t = Thread( target = cm.beginConnection, args=(host,port,callback_to_call))
		t.daemon = True
		t.start()

	def changeScreen(self, *args):
		#now switch to the screen 1
		print("Changing screen")
		self.clear_widgets()
		self.add_widget( MusicPlayer())

class ChooseFile(FloatLayout):
	select = ObjectProperty(None)
	cancel = ObjectProperty(None)

# Musicplayer gui : https://github.com/JasonHinds13/KVMusicPlayer
class MusicPlayer(Widget):

	directory = '' # location of songs folder
	nowPlaying = '' # Song that is currently playing
	songs = [] #List to hold songs from music directory
	player = '' # vlc player instance
	def __init__(self, **kwargs):
		super(MusicPlayer, self).__init__(**kwargs)	
		#vlc ready
		self.player = vlc.MediaPlayer()
		self.getpath()

	def getpath(self):
		try:
			f = open("sav.dat","r")
			self.ids.direct.text = str(f.readline())
			f.close()
			self.ids.searchBtn.text = "Scan"
			self.getSongs()
		except:
			self.ids.direct.text = ''
			
	def savepath(self, path):
		f = open("sav.dat","w")
		f.write(path)
		f.close()

	def dismiss_popup(self):
		self._popup.dismiss()

	def fileSelect(self):
		content = ChooseFile(select=self.select,
							 cancel=self.dismiss_popup)
		
		self._popup = Popup(title="Select Folder", content=content,
							size_hint=(0.9, 0.9))
		self._popup.open()

	def select(self, path):
		self.directory = path
		self.ids.direct.text = self.directory
		self.ids.searchBtn.text = "Scan"
		self.savepath(self.directory)
		self.getSongs()
		self.dismiss_popup()

	def playSong(self,bt):
		try:
			self.player.stop()
		except:
			pass
		finally:
			# self.nowPlaying = SoundLoader.load(self.directory+bt.text+'.mp3')
			try:
				# print "firstTry"
				self.nowPlaying = bt.text+'.mp3'
				track = bt.text
			except:
				# print "secondTry"
				self.nowPlaying = bt
				bt = bt.split('.')[:-1]
				bt = '.'.join(bt)
				track = bt
				# print("TRACK: ", track)
			# self.nowPlaying = bt.text+'.mp3'
			self.player.set_mrl(self.directory+track+'.mp3')
			self.player.play()
			self.ids.nowplay.text = track
	def pauseSong(self):
		if(self.player.is_playing()):
			self.ids.pauseButton.text = '>'
		else:
			self.ids.pauseButton.text = '||'
		self.player.pause()
	def nextSong(self):
		if(self.nowPlaying in self.songs):
			playIndex = self.songs.index(self.nowPlaying)+1
			if playIndex>len(self.songs)-1:
				playIndex=0
			self.playSong(self.songs[playIndex])
		else:
			print 'fail'			
	def prevSong(self):
		if(self.nowPlaying in self.songs):
			playIndex = self.songs.index(self.nowPlaying)-1
			self.playSong(self.songs[playIndex])
		else:
			print 'fail'			
		
	def getSongs(self):

		self.songs=[]
		self.ids.scroll.clear_widgets()
		self.directory = self.ids.direct.text #Directory entered by the user

		if self.directory == '':
			self.fileSelect()

		#To make sure that the directory ends with a '/'
		if not self.directory.endswith('/'):
			self.directory += '/'

		#Check if directory exists
		if not path.exists(self.directory):
			self.ids.status.text = 'Folder Not Found'
			self.ids.status.color = (1,0,0,1)

		else:

			self.ids.status.text = ''

			self.ids.scroll.bind(minimum_height=self.ids.scroll.setter('height'))

			#get mp3 files from directory
			for fil in listdir(self.directory):
				if fil.endswith('.mp3'):
					self.songs.append(fil)

			#If there are no mp3 files in the chosen directory
			if self.songs == [] and self.directory != '':
				self.ids.status.text = 'No Music Found'
				self.ids.status.color = (1,0,0,1)
					
			self.songs.sort()


			for song in self.songs:

					
				btn = Button(text=song[:-4], on_press=self.playSong)
				icon = Button(size_hint_x=None, width=50, background_down="ico.png", background_normal="ico.png")

				#Color Buttons Alternatively
				if self.songs.index(song)%2 == 0:
					btn.background_color=(0,0,1,1)
				else:
					btn.background_color=(0,0,2,1)
					
				self.ids.scroll.add_widget(icon) #Add icon to layout
				self.ids.scroll.add_widget(btn) #Add btn to layout

		
class BoomplayApp(App):
	def build(self):
	   return tabbedScreen() 
		


if __name__ == '__main__':
	BoomplayApp().run()