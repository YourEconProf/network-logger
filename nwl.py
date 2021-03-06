#!/usr/local/bin/python3

# home-network-logger periodically scans a home network
# to assist in diagnosing internet connectivity 
# problems

def pingOk(sHost):
	now = datetime.datetime.now()
	dt_string = now.strftime("%Y:%m:%d:%H:%M:%S")
	try:
		# create text call for debugging (why don't people do this on SO????)
		TEXT1 = "ping -{} 5 {}".format('n' if platform.system().lower()=="windows" else 'c', sHost)		
		#print(TEXT1)
		output = subprocess.run(TEXT1, shell=True,capture_output=True).stdout.decode('utf-8').splitlines()
		#print(output)
		stats = 'NA'
		dropped = 'NA'
		for i in range(len(output)):
			#print(outline[i])
			if re.search(r"%",output[i]):
				#print(i)
				dropped = re.findall(r'[0-9.]*%', output[i])
			if re.search(r"round-trip",output[i]):
				#print(output[i])
				stats = re.findall(r'[0-9./]* ms', output[i])[0]
				#print(stats)
				stats = re.sub(r' ms','',stats)
				#print(stats)
				stats = re.sub(r'/',',',stats)
				#print(type(stats))
		output = (dt_string + "," + platform.node() + "," + sHost + "," + stats + "," + dropped[0])

	except Exception:
		output = ("Oops: " + dt_string + " " + platform.node() + " " + sHost + " " + sys.exc_info()[0])

	#print(output)	
	return output

def writetolog(LOGFILE, text2write):
	fullpath = os.path.expanduser(LOGFILE)
	if os.path.exists(fullpath):
		append_write = 'a' # append if already exists
	else:
		append_write = 'w' # make a new file if not
	#print(append_write,"",fullpath)
	writefile = open(fullpath,append_write)
	writefile.write(text2write + '\n')
	writefile.close() 


PING_LIST = ['192.168.0.106', '192.168.1.1', 'www.google.com', '75.118.76.201' ]
SPEEDTEST = ''
LOGFILE   = '~/internetlog.txt'

import subprocess, platform, re, datetime, os, sys

for j in range(len(PING_LIST)):
	if PING_LIST[j] != "":
		results = pingOk(PING_LIST[j])
		#print(results)
		writetolog(LOGFILE, results)



