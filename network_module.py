# Import modules
import subprocess
import ipaddress
import netifaces as ni
import sys

def get_interfaces():
	print('Getting local interfaces...')
	interfaces = []
	for interface in ni.interfaces():
		if not interface.startswith(('lo', 'vir')):
			print('Found local interface {}'.format(interface))
			interfaces.append(interface)
	return interfaces

def get_local_ip():
	interfaces = get_interfaces()
	print('Getting local ip address...')
	for interface in interfaces:
		try:
			addr = ni.ifaddresses(interface)[2][0]['addr']
			print('Local ip address is {}'.format(addr))
			return addr
		except KeyError:
			print('Error: No local ip addresses found.')
	raise Exception

def get_subnet():
	ip = get_local_ip()
	subnet = '.'.join(ip.split('.')[:3]) + '.0/24'
	print('Subnet is {}'.format(subnet))
	return subnet

def scan_network(net_addr):

	# Prompt the user to input a network address
	# net_addr = input("Enter a network address in CIDR format(ex.192.168.1.0/24): ")

	# Create the network
	ip_net = ipaddress.ip_network(net_addr)

	# Get all hosts on that network
	all_hosts = list(ip_net.hosts())

	# Configure subprocess to hide the console window
	info = subprocess.STARTUPINFO()
	info.dwFlags |= subprocess.STARTF_USESHOWWINDOW
	info.wShowWindow = subprocess.SW_HIDE
	
	#LINUX/WIN ADJUSTS
	if sys.platform == "win32":
		no_of_ech_req = '-n'
	else:
		no_of_ech_req = '-c'
	# For each IP address in the subnet, 
	# run the ping command with subprocess.popen interface
	for i in range(len(all_hosts)):
		output = subprocess.Popen(['ping', no_of_ech_req, '1', '-w', '500', str(all_hosts[i])], stdout=subprocess.PIPE, startupinfo=info).communicate()[0]
		
		if "Destination host unreachable" in output.decode('utf-8'):
			# print(str(all_hosts[i]), "is Offline")
			pass
		elif "Request timed out" in output.decode('utf-8'):
			# print(str(all_hosts[i]), "is Offline")
			pass
		else:
			print(str(all_hosts[i]), "is Online")

def main():
	t = get_subnet()
	scan_network(t)

# main()	