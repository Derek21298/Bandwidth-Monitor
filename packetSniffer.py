#Sniffs only incoming TCP packet

import socket, sys
from struct import *
import sys
import time

#create an INET, STREAMing socket
try:
	s = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_TCP)
except socket.error or msg:
	print('Socket could not be created. Error Code : ' + str(msg[0]) + ' Message ' + msg[1])
	sys.exit()

dataTotal = 0
startTime = time.time()

while True:

	# Get a packet
	packet = s.recvfrom(65565)
	
	# Packet string from tuple
	packet = packet[0]

	# Take first 20 characters for ip header
	ip_header = packet[0:20]
	
	# Unpack the header and get length
	iph = unpack('!BBHHHBBH4s4s' , ip_header)
	version_ihl = iph[0]
	ihl = version_ihl & 4
	iph_length = ihl * 4
	
	# Get tcp header right after io header
	tcp_header = packet[iph_length:iph_length+20]
	
	# Unpack header and get length
	tcph = unpack('!HHLLBBHHH' , tcp_header)
	doff_reserved = tcph[4]
	tcph_length = doff_reserved >> 4
	
	# Size of the data is the packet size without the headers
	h_size = iph_length + tcph_length * 4
	data_size = len(packet) - h_size
	
	# Get the actual data
	data = packet[h_size:]

	dataTotal = dataTotal + sys.getsizeof(data)

	currTime = time.time()
	
#	if(currTime > (startTime + 5)):
#		print('5 Seconds have passed') 


	if(currTime > (startTime + 60)): 
			
		print('1 Minute has gone by!!!')
		print('Data size: ' + str(dataTotal) + ' bytes')
		dataTotal = 0
		startTime = time.time()
	
