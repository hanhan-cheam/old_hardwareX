
# from Database import database
import socket
import threading
from threading import Lock
from simple_chalk import greenBright, redBright, blueBright, cyanBright
import sys


# sys.path.append("..")

lock = threading.Lock()
connectionList = []
receivedMsgList = []
receivedBroadcastList = []


def startServer():
    try:
        s = socket.socket()
        port = 3700
        s.bind(('0.0.0.0', port))
        s.listen(5)
        print(greenBright("Server Listening"))
        newConnection = threading.Thread(target=onNewConnection, args=(s,), name="NewConnection")
        newConnection.start()
    except:
        print(redBright("Server Error"))


def onNewConnection(s,):
    try:
        while True:
            c, addr = s.accept()
            # get the name from database
            threadName = ""
            print("c and address : ","C -> ",c," ","ADDRESS : ",addr)
            newClient = threading.Thread(target=onNewClient, args=(c, addr), name=threadName)
            newClient.start()
    except:
        print(redBright("Connection Error"))


def onNewClient(c, addr, ):
    try:
        print("addr is ",addr)
        print("threadname is ", threading.currentThread().getName())
        connectionList.append([addr[0], addr[1], c, threading.currentThread().getName()])
        print("On new client ",connectionList)
        print(greenBright("--------  %s Connected  ------" % threading.currentThread().getName()))
        print(greenBright("  IP Address: %s\n  Port: %s " % (addr)))
        print(greenBright("--------------------------------------"))
        while True:
            reply = c.recv(1024).strip()
            decodedMsg = reply.decode()

            if(len(decodedMsg) == 0):
                # ping client to test connection, catch error if not connected
                c.send('ping'.encode())
            else:
                print(blueBright("Received Message: " + decodedMsg))
                splitedMsg = decodedMsg.split(",")

                if ('P' in splitedMsg[2]):
                    # Will be remove
                    if len(connectionList) != 0:
                        for conList in connectionList:
                            if(conList[3] == threading.currentThread().getName()):
                                conList[3] = str(splitedMsg[0]) + str(splitedMsg[1])
                    c.send((splitedMsg[0]+","+splitedMsg[1]+",P,SUCCESS;").encode())
                    c.send((splitedMsg[0]+","+splitedMsg[1]+",S;").encode())
                    lock.acquire()
                    receivedBroadcastList.append([splitedMsg[1], decodedMsg])
                    lock.release()
                elif ('S' in splitedMsg[2] or 'J' in splitedMsg[2]):
                    lock.acquire()
                    receivedBroadcastList.append([splitedMsg[1], decodedMsg])
                    lock.release()
                else:
                    lock.acquire()
                    receivedMsgList.append([addr[0], addr[1], decodedMsg])
                    print("receive message list here",receivedMsgList)
                    lock.release()
    except:
        onClientDisconnected(c, addr)


def onClientDisconnected(c, addr):
    try:
        disconnectedClient = getDisconnectDetails(c)
        c.close()
        # disconnectedClient = getClientDetails(threading.currentThread().getName())
        connectionList.remove(disconnectedClient)
        print(greenBright("-------  %s Disconnected  --------" % (threading.currentThread().getName())))
        print(greenBright("  IP Address: %s\n  Port: %s " % (addr)))
        print(greenBright("---------------------------------------"))
    except:
        print(redBright('Error in handle disconnected client'))


def getDisconnectDetails(conn):
    getClient = next(c for c in connectionList if c[2] == conn)
    return getClient


def getClientDetails(name):  #either here 
    getClient = next(c for c in connectionList if c[3] == name)    
    return getClient


def sendMsg(targetName, msg): #might here    
    try:
        targetClient = getClientDetails(targetName)
        targetClient[2].send(msg.encode())
        print(cyanBright("Sent Message: " + msg))
        return "Message sent"
    except Exception as e:
        print(redBright("sendMsg"))
        return "Client is not connected"


def processReply(name):    #either here 
    try:
        targetClient = getClientDetails(name)
        client_to_remove = next(c for c in receivedMsgList if c[0] == targetClient[0] and c[1] == targetClient[1])
        
        print(greenBright("process reply,client to remove"),client_to_remove)
        receivedMsgList.remove(client_to_remove)
        return client_to_remove[2]
    except:
        print(redBright("Error, Unable to obtain reply from client"))
