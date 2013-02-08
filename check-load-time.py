#!/usr/bin/python

# page load time check for graphite/carbon
# add urls into URLS dictionary file
# carbon is sent as PATHPREFIX.URLSKEY
#  ie. systems.host1.main.page

import subprocess
import time
import sys
from socket import socket

# define urls here in tuple to check
URLS = {'host1.main.page' : 'http://host1.local/',
        'host1-stage.people.page' : 'http://host1-stage.local/people', }

# define carbon information
CARBON_SERVER = 'graphite'
CARBON_PORT = 2013
PATHPREFIX = 'systems.'

# get the time
def getTimeNow():
    timeNow = int ( time.time() )
    return timeNow

# send data to carbon
def sendtoCarbon(nowtime):

# create socket, and check if port open
  sock = socket()
  try:
    sock.connect( (CARBON_SERVER,CARBON_PORT) )
  except:
    print "Couldn't connect to %s on port %d, is carbon running?" % (CARBON_SERVER, CARBON_PORT)
    sys.exit(1)

  print  "Connected to %s on port %d" % (CARBON_SERVER, CARBON_PORT)
  sendlines = []

# iterate through dictionary of urlnames, and urls to check
# spanws time & lynx -dump to get the time for page load
  for k, v in URLS.iteritems():
    p = subprocess.Popen(('time -p lynx -dump %s' % v), shell=True, 
                          stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

# grab lines, and append the 3rd line from the end to real_time
# this line contains the real output from [time] 
# append to sendlines[], with the output that carbon wants

    lines = p.stdout.readlines()
    real_time = lines[(len(lines)-3)].rstrip()
    sendlines.append("%s%s %s %d" % (PATHPREFIX,k,real_time[5:],nowtime))

# join it all up into message
# print it for the user to see
  message = '\n'.join(sendlines) + '\n' 
  print '-' * 80
  print message
  print

# send all the data to carbon
  sock.sendall(message)
# close the socket
  sock.close()

if __name__ == '__main__': 

# get current unix time
  timeNow = getTimeNow()
# send data to carbon
  sendtoCarbon(timeNow)
