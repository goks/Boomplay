from kivy.app import App

from kivy.uix.widget import Widget
from kivy.uix.screenmanager import ScreenManager, Screen, SlideTransition
from threading import Thread,Event
#local imports
import network_module as nm
import server_TCP as sm
import client_TCP as cm


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

class BoomplayApp(App):
	def build(self):
	   return tabbedScreen() 
		


if __name__ == '__main__':
	BoomplayApp().run()