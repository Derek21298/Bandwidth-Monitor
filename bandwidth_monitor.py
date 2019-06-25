# bandwidth_monitor.py
# 
# Author: Derek Haas
# Description: Use psutil to get the net io counters to report data usage
#
# Date: June 12 2019
#

import psutil
import time

print('Gathering Information on Network Interfaces...')

# Get the all the network stats for the first calculation
net_stats = psutil.net_io_counters(pernic=True)

# Initialize arrays
key_list = []
sent_start = [0, 0, 0]
received_start = [0, 0, 0]
sent_curr = [0, 0, 0]
received_curr = [0, 0, 0]
sent = [0, 0, 0]
received = [0, 0, 0]

# Get the network interfaces from the dictionary
for key in net_stats:
	
	print('Network Interface Detected!: {}'.format(key))
	key_list.append(key)


# Get the start bytes sent and received of all interfaces
for i in range(len(net_stats)):

	sent_start[i] = net_stats[key_list[i]][1]
	received_start[i] = net_stats[key_list[i]][2]

# Begin to get data every minute
print('Starting to Collect Bandwidth Data...')

startTime = time.time()
periodTime = time.time()

total_sent = 0
total_received = 0

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
		
		for i in range(len(net_stats)):
	
			sent_curr[i] = net_stats[key_list[i]][1]
			received_curr[i] = net_stats[key_list[i]][2]
			
			sent[i] = sent_curr[i] - sent_start[i]
			received[i] = received_curr[i] - received_start[i] 	

			print('Network Interface: {}\nBytes Sent: {}\t\t\tBytes Recieved: {}\n'.format(key_list[i], sent[i], received[i]))

			total_sent = total_sent + sent[i]
			total_received = total_received + received[i]

		# SENT DATA
		# If the data sent is between 1k and 1M print as 1 kB
		if((total_sent > 1000) and (total_sent < 1000000)):
			total_sent = total_sent * 1e-3
			print('Data SENT in the past minute: %.2f KB'%total_sent)
		
		# If the data sent is between 1M and 1G print as 1M
		elif((total_sent > 1000000) and (total_sent < 1000000000)):
			total_sent = total_sent * 1e-6
			print('Data SENT in the past minute: %.2f MB'%total_sent)

		# If the data sent is between 1G and 1T print as 1G
		elif((total_sent > 1000000000) and (total_sent < 1000000000000)):
			total_sent = total_sent * 1e-9
			print('Data SENT in the past minute: %.2f GB'%total_sent)

		# Else just print as bytes
		else:
			print('Data SENT in the past minute: %d B'%total_sent)

		# RECEIVED DATA
		# If the data received is between 1k and 1M print as 1 kB
		if((total_received > 1000) and (total_received < 1000000)):
			total_received = total_received * 1e-3
			print('Data RECEIVED in the past minute: %.2f KB'%total_received)
		
		# If the data received is between 1M and 1G print as 1M
		elif((total_received > 1000000) and (total_received < 1000000000)):
			total_received = total_received * 1e-6
			print('Data RECEIVED in the past minute: %.2f MB'%total_received)

		# If the data received is between 1G and 1T print as 1G
		elif((total_received > 1000000000) and (total_received < 1000000000000)):
			total_received = total_received * 1e-9
			print('Data RECEIVED in the past minute: %.2f GB'%total_received)

		# Else just print as bytes
		else:
			print('Data RECEIVED in the past minute: %d B'%total_received)
		
		# Reset all the variables
		total_sent = 0
		total_received = 0
		startTime = time.time()
		periodTime = time.time()
		
		# Set the start values as the old current values
		for i in range(len(net_stats)):
	
			sent_start[i] = sent_curr[i]
			received_start[i] = received_curr[i]




