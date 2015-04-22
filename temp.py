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















temp=""



destinations=[["172.22.22.130",8008,11111],["172.22.22.131",8008,11111], ["172.22.22.132",8008,11111], ["172.22.22.133",8008,11111]]


