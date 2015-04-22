#!/usr/bin/python


import socket
import sys
import time


import errno

import threading


class StreamHandler:
    a = None
    b = None
    run=True
    debug=False
    coldStart=False
    ##Divisor - Send 1/n, divisor=n packets
    divisor=10
    
    
    ##Packet buffer
    dataBuffer=[]
    ##Destinations List  
    destinations=[]
    perDestEnable=[]
    
    ###Threads list
    threads=[]
    
    ##Sockets
    INsock = None
    OUTsock = None



    def __init__(self, listenIP, listenPort):
        UDP_IP = listenIP
        UDP_PORT = listenPort
        INsock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        INsock.bind((UDP_IP, UDP_PORT))
        #####
        OUTsock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        
        print self.a
        self.a = a
        self._x = 123;
        self.__y = 123;
        b = 'meow'
        





####Functions




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
    def addDest(ip,streamDestPort,monitorClientPort):
        destinations.append([ip,StreamDestPort,monitorClientPort])
        perDestEnable.append(0)
        newthread = checkHost(destinations.index([ip,StreamDestPort,monitorClientPort]))
        newthread.start()
        threads.append(newthread)





###### classes
    class checkHost(threading.Thread):
    class inputHandler(threading.Thread):
    class outputHandler(threading.Thread):















temp=""



destinations=[["172.22.22.130",8008,11111],["172.22.22.131",8008,11111], ["172.22.22.132",8008,11111], ["172.22.22.133",8008,11111]]



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
