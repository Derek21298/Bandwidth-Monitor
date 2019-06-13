# bandwidth_monitor.py
# 
# Author: Derek Haas
# Description: Sniff incoming and outgoing packets to determine the data size
#
# Date: June 12 2019
#

import socket, sys
from struct import *
import sys
import time

# Create an INET, STREAMing socket
try:
	s = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_TCP)
except socket.error or msg:
	print('Socket could not be created. Error Code : ' + str(msg[0]) + ' Message ' + msg[1])
	sys.exit()

# Time is epoch time (January 1 1970)
dataTotal = 0
startTime = time.time()

# Always get packets
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

	# If 60 seconds has passed, update the data
	currTime = time.time()
	if(currTime > (startTime + 60)): 
			
		print('1 Minute has gone by!!!')

		# If the data sent is between 1k and 1M print as 1 kB
		if((dataTotal > 1000) and (dataTotal < 1000000)):
			dataTotal = dataTotal * 1e-3
			print('Data sent in the past minute: %.2f KB'%dataTotal)
		
		# If the data sent is between 1M and 1G print as 1M
		elif((dataTotal > 1000000) and (dataTotal < 1000000000)):
			dataTotal = dataTotal * 1e-6
			print('Data sent in the past minute: %.2f MB'%dataTotal)

		# If the data sent is between 1G and 1T print as 1G
		elif((dataTotal > 1000000000) and (dataTotal < 1000000000000)):
			dataTotal = dataTotal * 1e-9
			print('Data sent in the past minute: %.2f GB'%dataTotal)

		# Else just print as bytes
		else:
			print('Data sent in the past minute: %d B'%dataTotal)

		dataTotal = 0
		startTime = time.time()
