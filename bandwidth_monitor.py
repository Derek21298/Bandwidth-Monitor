# bandwidth_monitor.py
# 
# Author: Derek Haas
# Description: Use psutil to get the net io counters to report data usage
#
# Date: June 12 2019
#

import psutil
import time

print('Getting preliminary data...')

# Get the all the network stats for the first calculation
net_stats = psutil.net_io_counters(pernic=True)

# Print the net stats (mainly for debugging)
'''
print('Network Interface: lo\t\tBytes Sent: %d'%net_stats['lo'][1])
print('Network Interface: lo\t\tBytes Received: %d\n'%net_stats['lo'][2])
print('Network Interface: enp4s0\tBytes Sent: %d'%net_stats['enp4s0'][1])
print('Network Interface: enp4s0\tBytes Received: %d\n'%net_stats['enp4s0'][2])
print('Network Interface: wlp5s0\tBytes Sent: %d'%net_stats['wlp5s0'][1])
print('Network Interface: wlp5s0\tBytes Received: %d\n'%net_stats['wlp5s0'][2])
'''

# Get the bytes sent and received for the different interfaces
lo_sent_start = net_stats['lo'][1]
lo_received_start = net_stats['lo'][2]
enp_sent_start = net_stats['enp4s0'][1]
enp_received_start = net_stats['enp4s0'][2]
wlp_sent_start = net_stats['wlp5s0'][1]
wlp_received_start = net_stats['wlp5s0'][2]


# Begin to get data every minute
print('Starting to collect data...')

startTime = time.time()
periodTime = time.time()
while True:

	currTime = time.time()

	# If 2 seconds pass, print a '.' as a status bar
	if(currTime > (periodTime + 2)):
		print('.', end='', flush=True)
		periodTime = time.time()
		

	# If 60 seconds has passed, print the total data and reset
	if(currTime > (startTime + 60)):
		 
		print('\n')	
		print('1 Minute has gone by!!!\n')

		# Get the current data
		net_stats = psutil.net_io_counters(pernic=True)
		
		lo_sent_curr = net_stats['lo'][1]
		lo_received_curr = net_stats['lo'][2]
		enp_sent_curr = net_stats['enp4s0'][1]
		enp_received_curr = net_stats['enp4s0'][2]
		wlp_sent_curr = net_stats['wlp5s0'][1]
		wlp_received_curr = net_stats['wlp5s0'][2]

		lo_sent = lo_sent_curr - lo_sent_start
		enp_sent = enp_sent_curr - enp_sent_start
		wlp_sent = wlp_sent_curr - wlp_sent_start

		# (Current - Start) is the data sent over a minute
		lo_received = lo_received_curr - lo_received_start
		enp_received = enp_received_curr - enp_received_start
		wlp_received = wlp_received_curr - wlp_received_start

		print('Network Interface: lo\t\tBytes Sent: %d'%lo_sent)
		print('Network Interface: lo\t\tBytes Received: %d\n'%lo_received)
		print('Network Interface: enp4s0\tBytes Sent: %d'%enp_sent)
		print('Network Interface: enp4s0\tBytes Received: %d\n'%enp_received)
		print('Network Interface: wlp5s0\tBytes Sent: %d'%wlp_sent)
		print('Network Interface: wlp5s0\tBytes Received: %d\n'%wlp_received)

		dataTotal = lo_sent + enp_sent + wlp_sent
		
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

		# Reset all the variables
		dataTotal = 0
		startTime = time.time()
		periodTime = time.time()
		
		lo_sent_start = lo_sent_curr
		lo_received_start = lo_received_curr
		enp_sent_start = enp_sent_curr
		enp_received_start = enp_received_curr
		wlp_sent_start = wlp_sent_curr
		wllp_received_start = wlp_received_curr





