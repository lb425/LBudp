#!/usr/bin/python

import socket
import sys
import time
import errno
import threading

class StreamHandler:

    def __init__(self, listenIP, listenPort):
        setUp()
        UDP_IP = listenIP
        UDP_PORT = listenPort
        INsock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        INsock.bind((UDP_IP, UDP_PORT))
        #####
        OUTsock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        print("1")
        ##ADD destinations!
        ##Then start()
        





####Functions

    def start(self):
        newthread = outputHandler(self.OUTsock)
        newthread.start()
        self.threads.append(newthread)
        time.sleep(5)
        newthread = inputHandler(self.INsock)
        newthread.start()
        self.threads.append(newthread)
        
    def stop(self):
        self.run=0
        for t in self.threads:
        t.join()

###Setup Variables , called by __init__
    def setUp(self):
        self.run=True
        self.debug=False
        self.coldStart=False
        ##Divisor - Send 1/n, divisor=n packets
        self.divisor=10
    
    
        ##Packet buffer
        self.dataBuffer=[]
        ##Destinations List  
        self.destinations=[]
        self.perDestEnable=[]
        
        ###Threads list
        self.threads=[]
        
        ##Sockets
        self.INsock = None
        self.OUTsock = None


    ##Check results of CPU test
    def checkResults(data):
        toRet=0
        temp = data.split('-')
        if debug:
            print temp
        if temp[0]=="1" and temp[1]=="1" and int(temp[2])<95 and int(temp[3])<90:
            toRet=1
        return toRet
#       return 1


    #function: addDest(ip,streamDestPort,monitorClientPort)
    #Example: addDest("172.22.22.130", 11111, 8008)
    #Created entry in destinations list with format [ip,monitorClientPort,streamDestPort]
    def addDest(self,ip,streamDestPort,monitorClientPort):
        self.destinations.append([ip,StreamDestPort,monitorClientPort])
        self.perDestEnable.append(0)
        newthread = checkHost(self.destinations.index([ip,StreamDestPort,monitorClientPort]))
        newthread.start()
        self.threads.append(newthread)





###### classes
    class checkHost(threading.Thread):
    class inputHandler(threading.Thread):
    class outputHandler(threading.Thread):



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
                                data = sock.recv(1024)
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
                global dataBuffer
                global run

        ###Warm the receivers  with 1010 for decimation
                if coldStart:
                        for i in range(1000):
                                for j in range(1010-i):
                                        data, addr = self.sock.recvfrom(1024)
                                for j in 3*range(len(destinations)):
                                        data, addr = self.sock.recvfrom(1024) # buffer size is 1024 bytes
                                        dataBuffer.append(data)

                while run:
                        #DECIMATION!!!!                         Divisor
                        for k in range(divisor-1):
                                data, addr = self.sock.recvfrom(1024) # 2

                        #gather data
                        data, addr = self.sock.recvfrom(1024) # buffer size is 1024 bytes
                        dataBuffer.append(data)

class outputHandler(threading.Thread):
        def __init__(self, sock):
                threading.Thread.__init__(self)
                self.socket=sock
        def run(self):
                global dataBuffer
                global destinations
                global perDestEnable
                global run
                OUTsock = self.socket
                while run:
                        if len(dataBuffer)>len(destinations):
                                for i in range(len(destinations)):
                                        if perDestEnable[i] == 1:
                                                tmp=destinations[i]
                                                OUTsock.sendto(dataBuffer.pop(), (tmp[0], tmp[2]))
                        else:
                                time.sleep(.1)











temp=""



destinations=[["172.22.22.130",8008,11111],["172.22.22.131",8008,11111], ["172.22.22.132",8008,11111], ["172.22.22.133",8008,11111]]


