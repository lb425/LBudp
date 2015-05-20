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
UDP_PORT = 5005
OUTUDP_IP = "172.22.22.130"
temp=""
INsock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
INsock.bind((UDP_IP, UDP_PORT))
dataBuffers=[]
#####
OUTsock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
######


destinations=[["172.22.22.130",8008,UDP_PORT],["172.22.22.131",8008,UDP_PORT], ["172.22.22.132",8008,UDP_PORT], ["172.22.22.133",8008,UDP_PORT],["172.22.22.134",8008,UDP_PORT], ["172.22.22.135",8008,UDP_PORT], ["172.22.22.136",8008,UDP_PORT],["172.22.22.137",8008,UDP_PORT], ["172.22.22.138",8008,UDP_PORT], ["172.22.22.139",8008,UDP_PORT]]
perDestEnable=[]
for i in destinations:
        perDestEnable.append(0)
threads=[]
#exit()

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
                # Connect the socket to the port where the server is listening
                server_address = (destinations[ID][0], destinations[ID][1])

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
        def __init__(self, socket):
                threading.Thread.__init__(self)
                self.sock=socket
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
                                        dataBuffers.append(data)

                while run:
                        #DECIMATION!!!!                         Divisor
                        for k in range(divisor-1):
                                data, addr = self.sock.recvfrom(bufferSize) # 2

                        #gather data
                        data, addr = self.sock.recvfrom(bufferSize) # buffer size is "bufferSize" bytes
                        dataBuffers.append(data)

class outputHandler(threading.Thread):
        def __init__(self, sock):
                threading.Thread.__init__(self)
                self.socket=sock
        def run(self):
                global dataBuffers
                global destinations
                global perDestEnable
                global run
                OUTsock = self.socket
                while run:
                        if len(dataBuffers)>len(destinations):
                                for i in range(len(destinations)):
                                        if perDestEnable[i] == 1:
                                                tmp=destinations[i]
                                                OUTsock.sendto(dataBuffers.pop(), (tmp[0], tmp[2]))
                        else:
                                time.sleep(.1)




for i in range(len(destinations)):
        newthread = checkHost(i)
        newthread.start()
        threads.append(newthread)

time.sleep(5)

newthread = outputHandler(OUTsock)
newthread.start()
threads.append(newthread)

time.sleep(5)
newthread = inputHandler(INsock)
newthread.start()
threads.append(newthread)

for t in threads:
        t.join()
