# bandwidth_monitor.py
# 
# Author: Derek Haas
# Description: Use psutil to get the net io counters to report data usage
#
# Date: June 26  2020
#

import psutil
import time

print('Getting preliminary data...')

# Get the all the network stats for the first calculation
netStats = psutil.net_io_counters(pernic=True)

# Get the bytes sent and received for the different interfaces
sentStart = []
receivedStart = []
for interface in netStats:
    sentStart.append(netStats[interface][1])
    receivedStart.append(netStats[interface][2])

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
        print('1 Minute has gone by!\n')

        # Get the current data
        netStats = psutil.net_io_counters(pernic=True)
        
        dataTotal = 0
        for i,interface in enumerate(netStats):
            sentData = netStats[interface][1] - sentStart[i]
            receivedData = netStats[interface][2] - receivedStart[i]
        
            print('Network Interface: {}\t\tBytes Sent: {}'.format(interface, sentData))
            print('Network Interface: {}\t\tBytes Received: {}'.format(interface, receivedData))
        
            dataTotal = dataTotal + sentData
        
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
        
        # Get the bytes sent and received for the different interfaces
        sentStart = []
        receivedStart = []
        for interface in netStats:
            sentStart.append(netStats[interface][1])
            receivedStart.append(netStats[interface][2])
		
