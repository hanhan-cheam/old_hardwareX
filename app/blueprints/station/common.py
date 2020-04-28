
from flask import Flask, jsonify, request
import time,json
from simple_chalk import greenBright, redBright, blueBright
from app import server
import eventlet
eventlet.monkey_patch()
from ...database import station as db_station
from ...database import bin as db_bin
from app import socketio,app

def jsonFormat(msg, error):
    try:
        json = {
            "data": msg,
            "error": error

        }
        return json
    except Exception as e:
        print(redBright(e))


def checkRequest(stationID, msg):
    print("common check request",stationID," ---- ", msg)
    try:
        for i in range(5):
            reply = None
            timeout = time.time() + 5
            msgToSend = msg
            print("msgToSend cehck request ",msgToSend)
            # response = "Message sent" #try
            response = server.sendMsg("ST"+str(stationID), msgToSend)
            print("response is msg sent ma ",response)
            time.sleep(0.1)
            if(response == "Message sent"):
                print("response is not else",response,"and reply is",reply)
                while reply is None:
                    if time.time() > timeout:  # Handle timeout waiting for client repsonse
                        reply = "Request Timeout"

                    # If there are messages in queue, check them
                    if len(server.receivedMsgList) != 0:
                        reply = server.processReply("ST"+str(stationID))
                        reply = reply.replace(";", "")
                        splitedReply = reply.split(',')
                        print("splitedReply,is", splitedReply)
                        return splitedReply
            else:
                print("response is else",response)
                reply = response
                return reply

        reply = "Requet Timeout"
        return reply
    except Exception as e:
        print(redBright("error checkRequest"))
        print("checkRequest",redBright(e))




def broadcastLoop():  
    try:
        while True:
            eventlet.sleep(0.1)
            if(len(server.receivedBroadcastList) != 0):
                reply = server.receivedBroadcastList.pop(0)
                msg = reply[1].replace(";", "")
                splitedReply = msg.split(",")
                if ("P" in splitedReply[2]):
                    pairSuccess(splitedReply[1])
                elif ("S" in splitedReply[2]):
                    bin = splitedReply[3].split("|")
                    print("split reply : ",splitedReply)
                    print("bin is boradcast",bin)
                    for i in range(len(bin)):
                        if(bin[i] != ""):
                            db_bin.InsertUpdateBin(bin[i], i, reply[0])
                        else:
                            db_bin.DeleteBin(reply[0], i)
                    updateStatus(bin, int(reply[0]))
                elif("J" in splitedReply[2]):
                    job_info = splitedReply[4].split('|')
                    msgToSend = "ACK,"+reply[1]
                    server.sendMsg("ST"+splitedReply[1], msgToSend)
                    requestReply = jsonFormat({
                        "station_id": int(splitedReply[1]),
                        "job_id": int(splitedReply[3]),
                        "status": "COMPLETED",
                        "bin_id": job_info[3]}, "")
                    with app.test_request_context('/'):
                        socketio.emit("move", requestReply, broadcast=True, namespace='/station')
    # except:
    #     print(redBright("executeStatus Error"))
    except Exception as e:
        print(e)


def updateStatus(bin, station):
    try:
        statusReply = jsonFormat({"station_id": int(station), "bins": bin}, "")
        with app.test_request_context('/'):
            socketio.emit("status", statusReply, broadcast=True, namespace='/station')
        print("replied with status")
    except:
        print(redBright("Socket Status Error"))


def pairSuccess(id):
    try:
        print("broadcasting pairing")
        statusReply = jsonFormat({"station_id": int(id)}, "")
        with app.test_request_context('/'):
            socketio.emit('pairing', statusReply, broadcast=True, namespace='/station')
    except Exception as e:
        print(redBright(e))