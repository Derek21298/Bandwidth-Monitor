# internet_speedtest.py
# 
# Author: Derek Haas
# 
# Description: Use speedtest-cli to collect information about download,
# speed, upload speed, and ping
#
# Date: June 10 2019
#

import speedtest
import time

# Function to conduct the speetest
def test(): 

	# Get the best server and get the results
	s = speedtest.Speedtest()
	s.get_servers()
	s.get_best_server()
	s.download()
	s.upload()
	
	result = s.results.dict()

	# Results are a dictionary
	return result["download"], result["upload"], result["ping"]

def main():

	start = time.time()
	# Get the download, upload, and ping from the test
	download, upload, ping = test()

	# convert to Mbps
	download = download * 1e-6
	upload = upload * 1e-6
	
	stop = time.time()

	print('Download: {}\nUpload: {}\nPing: {}'.format(download, upload, ping))
	print('Total Time: {}'.format(stop-start))

	# Write to a csv
	with open('log.csv', 'w') as file:
		file.write('Download \t Upload \t Ping\n')
		file.write('%.3f'%download);
		file.write(' Mbps\t ')
		file.write(str('%.3f'%upload))
		file.write(' Mbps\t ')
		file.write(str(ping))
		file.write(' ms\n')

		file.close()

if __name__ == '__main__':
	main()	






