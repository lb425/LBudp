#!/usr/bin/python


import socket
import sys
import time


import errno

import threading


run=True
debug=False
coldStart=False
##Divisor - Send 1/n, divisor=n packets
divisor=1

##Server junk
bufferSize=1600

UDP_IP = "0.0.0.0"
GANGLIA_PORT = 8008
temp=""
dataBuffers=[]
#####

ports=[5005]
sockets=[]
destinations=[["172.22.22.130"],["172.22.22.131"], ["172.22.22.132"], ["172.22.22.133"],["172.22.22.134"], ["172.22.22.135"], ["172.22.22.136"],["172.22.22.137"], ["172.22.22.138"], ["172.22.22.139"]]
perDestEnable=[]
for i in destinations:
        perDestEnable.append(0)
threads=[]
#exit()

##Set up everything for multiple ports
for port in ports:
        tmp=[]
        dataBuffers.append(tmp)
        tSock=socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        tSock.bind((UDP_IP, port))
        sockets.append(tSock)
        

##Future Thread Variables


def checkResults(data):
        toRet=0
        temp = data.split('-')
        if debug:
                print temp
        if temp[0]=="1" and temp[1]=="1" and int(temp[2])<95 and int(temp[3])<90:
                toRet=1
        return toRet
#       return 1


class checkHost(threading.Thread):
        def __init__(self, destID):
                threading.Thread.__init__(self)
                self.ID = destID
        def run(self):
                decision = 0
                ID=self.ID
                global run
                global GANGLIA_PORT
                # Connect the socket to the port where the server is listening
                server_address = (destinations[ID][0], GANGLIA_PORT)

                while run:
                        # Create a TCP/IP socket
                        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                #       print destinations[ID][0]
                        time.sleep(1)
                        try:
                #               if decision:
                #                       print "1"
                #               else:
                #                       print "0"

                                sock.connect(server_address)
                                sock.settimeout(1)
                                time.sleep(1)
                                data = sock.recv(bufferSize)
                                decision=checkResults(data)
                        except socket.error, v:
                                decision = 0
                        finally:
                                perDestEnable[ID]=decision
                                sock.close()

class inputHandler(threading.Thread):
        def __init__(self, socket, streamID):
                threading.Thread.__init__(self)
                self.sock=socket
                self.streamID=streamID
        def run(self):
                global dataBuffers
                global run

        ###Warm the receivers  with 1010 for decimation
                if coldStart:
                        for i in range(1000):
                                for j in range(1010-i):
                                        data, addr = self.sock.recvfrom(bufferSize)
                                for j in 3*range(len(destinations)):
                                        data, addr = self.sock.recvfrom(bufferSize) # buffer size is "bufferSize" bytes
                                        dataBuffers[streamID].append(data)

                while run:
                        #DECIMATION!!!!                         Divisor
                        for k in range(divisor-1):
                                data, addr = self.sock.recvfrom(bufferSize) # 2

                        #gather data
                        data, addr = self.sock.recvfrom(bufferSize) # buffer size is "bufferSize" bytes
                        dataBuffers[streamID].append(data)

class outputHandler(threading.Thread):
        def __init__(self, sock, streamID):
                threading.Thread.__init__(self)
                self.socket=sock
                self.streamID=streamID
        def run(self):
                global dataBuffers
                global destinations
                global perDestEnable
                global run
                global ports
                OUTsock = self.socket
                while run:
                        if len(dataBuffers[streamID])>len(destinations):
                                for i in range(len(destinations)):
                                        if perDestEnable[i] == 1:
                                                tmp=destinations[i]
                                                OUTsock.sendto(dataBuffers[streamID].pop(), (destinations[i][0], ports[self.streamID]))
                        else:
                                time.sleep(.1)




for i in range(len(destinations)):
        newthread = checkHost(i)
        newthread.start()
        threads.append(newthread)

time.sleep(5)

newthread = outputHandler(sockets[0], 0)
newthread.start()
threads.append(newthread)

time.sleep(5)
newthread = inputHandler(sockets[0], 0)
newthread.start()
threads.append(newthread)

for t in threads:
        t.join()
