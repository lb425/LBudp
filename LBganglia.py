#!/usr/bin/python

#output format opinion-processesrunning-instantaneousload-weightedaverageload
##TODO:
##UDP LISTENER
##Integrate heartbeat info into logic
import os
import time
##For CPU Load     pkg:python-psutil
import psutil

##For threading
import threading

##For TCP Server
import socket
import math

##TCP Server VAriables
## Whitelist of IPs allowed to access client
whitelist = ["127.0.0.1","172.22.22.10","172.22.22.11","172.22.22.12","172.22.22.24"]
host = "0.0.0.0"
port = 8008


##System Check Variables
processRunning = False
cpuHistory = [100,100,100,100,100]
cpuHistoryWeights= [7,6,5,4,3]
cpuWeightSum=sum(cpuHistoryWeights)
cpuLoadFigure = 0
##Process to check status of (checks for process name)
processName = 'logstash'
##Interval between CPU load checks
cpuTestInterval=.5
currentLoad=100

##Swiss variables
running=True
threads = []
opinion = 1

#Heartbeat info
useHeartbeat=0
lastEpoch=0
heartbeatTimeout=15   ##Max seconds since last heartbeat
heartbeatUDPport=61234

if useHeartbeat == 1:
    import time


class ClientThread(threading.Thread):

    def __init__(self, ip, port, socket):
        threading.Thread.__init__(self)
        self.ip = ip
        self.port = port
        self.socket = socket
        #print "[+] New thread started for "+ip+":"+str(port)


    def run(self):
        global whitelist
        global currentLoad
        global cpuLoadFigure
        global processRunning

       # print "Connection from : "+ip+":"+str(port)

        if ip not in whitelist:
                self.socket.close()
        else:
#               print "hey"
#                self.socket.send("\nWelcome to the server\n\n")

#               while len(data):
#                       data = self.socket.recv(2048)
                self.socket.send(str(opinion)+"-"+("1" if processRunning else "0")+"-"+str(currentLoad)+"-"+str(cpuLoadFigure))

                self.socket.close()
        #print "Client disconnected..."
#        thread.exit()

def checkProcess(pName):
        global processRunning
        tmp = os.popen("ps -Af").read()
        proccount = tmp.count(pName)

        if proccount > 0:
                processRunning = True
        else:
                processRunning = False

def checkCPU():
        global currentLoad
        global cpuHistory
        global cpuHistoryWeights
        global cpuWeightSum
        global cpuLoadFigure
        currentLoad = psutil.cpu_percent(interval=cpuTestInterval)
        cpuHistory = cpuHistory[:len(cpuHistory)-1]
        cpuHistory.insert(0,currentLoad)

        sum=0
        for x in range(0,len(cpuHistory)):
                sum = sum + cpuHistory[x]*cpuHistoryWeights[x]
        cpuLoadFigure = int(math.ceil(sum/cpuWeightSum))
        currentLoad = int(math.ceil(currentLoad))
        
def compareHeartbeatTime():
    global lastEpoch
    currentEpoch= int(time.time())
    return abs(currentEpoch-lastEpoch)

class checkSystem(threading.Thread):
        def __init__(self):
                threading.Thread.__init__(self)
        def run(self):
                while running:
#                       time.sleep(1)
                        checkProcess(processName)
                        checkCPU()
                       # print "history: " + str(cpuHistory)
                       # print "current: " + str(checkCPU())
                       # print "Load Figure: " + str(cpuLoadFigure)
                       # print "============="
                       
class listenHeartbeat(threading.Thread):
        def __init__(self, socket):
                threading.Thread.__init__(self)
                self.socket = socket
        def run(self):
                while running:
                    data, addr = self.socket.recvfrom(1024)
                    print data

if __name__ == "__main__":
        #Start monitoring thread
        monitorThread = checkSystem()
        monitorThread.start()
        threads.append(monitorThread)

        if useHeartbeat == 1:
            udpsock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            udpsock.bind(("127.0.0.1", heartbeatUDPport))
            heartbeatMonitorThread=listenHeartbeat(udpsock)
            heartbeatMonitorThread.start()
            threads.append(heartbeatMonitorThread)

        tcpsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        tcpsock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        tcpsock.bind((host,port))

        #Create sockets
        while running:
                tcpsock.listen(4)
        #       print "\nListening for incoming connections..."
                (clientsock, (ip, port)) = tcpsock.accept()
                newthread = ClientThread(ip, port, clientsock)
                newthread.start()
#               threads.append(newthread)


#       for t in threads:
#               t.join()




#Thread
##Weighted CPU time, check against threshhold
##Check for process

#Thread
##Respond to requests





#STATE Changes
#No Process to Process
#Detect process now running
#Wait tiem (60 seconds?)
#Check for Process again
#Signal ready

###process_names = [proc.name() for proc in psutil.process_iter()]
###http://stackoverflow.com/questions/16326529/python-get-process-names-cpu-mem-usage-and-peak-mem-usage-in-windows

