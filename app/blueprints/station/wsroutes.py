from app import socketio
from simple_chalk import greenBright, redBright, blueBright
from app import server
from .common import jsonFormat,checkRequest
# from flask_socketio import SocketIO, emit
from ...database import station as db_station
from ...database import bin as db_bin
import time

@socketio.on('connect')
def handleConnection():
    try:
        print('A socketio client has connected.')
    except:
        print(redBright("Socketio Connection Error"))


@socketio.on('disconnect')
def handleDisconnect():
    try:
        print('A socketio client has disconnected.')
    except:
        print(redBright("Socketio Disconnect Error"))


@socketio.on("status", namespace='/station')
def requestStatus(data):
    try:
        data = request.get_json()
        msgToSend = "ST,"+str(data['station_id'])+",S;"
        reply = server.sendMsg("ST"+str(data['station_id']), msgToSend)
        return "Np problem"
    except:
        print(redBright("Unable to manually request Status"))


@socketio.on('request', namespace="/station")
def RequestStation(data):
    print("i am in")
    try:
        if (data['action'] == "drop"):
            action = "D"
        elif (data['action'] == "pick"):
            action = "P"

        msgToSend = "ST,"+str(data['station_id'])+",R," + str(data['job_id']) + ","+str(data['position'])+"|"+action+"|" + str(data['bin_id'])+";"
        reply = checkRequest(data['station_id'], msgToSend)
        if type(reply) is list:
            if (reply[2] == 'A'):
                requestReply = jsonFormat({
                    "station_id": data['station_id'],
                    "job_id": data['job_id'],
                    "status": "true",
                    "message": "Approved"}, "")
            else:
                requestReply = jsonFormat({
                    "station_id": data['station_id'],
                    "job_id": data['job_id'],
                    "status": "false",
                    "message": "Denied"}, "")
        else:
            requestReply = jsonFormat({
                "station_id": data['station_id'],
                "job_id": data['job_id'],
                "status": "false",
                "message": "Denied"}, reply)
        socketio.emit("request", requestReply, namespace='/station')
        # emit("request", requestReply)
    except Exception as e:
        print (redBright(e))
    # except:
    #     print(redBright("Endpoint RequestStation Error"))


@socketio.on("update", namespace='/station')  # Add Bin at index 0
def updateStation(data):
    try:
        if (data['action'] == "drop"):
            action = 'D'
        elif (data['action'] == "pick" or data['action'] == "Pick"):
            action = 'P'

        msgToSend = "ST,"+str(data['station_id'])+",U," + str(data['job_id']) + ","+str(data['position'])+"|"+action+"|" + data['bin_id']+";"
        reply = checkRequest(data['station_id'], msgToSend)

        if type(reply) is list:
            if(reply[0] == "ACK"):
                splitData = reply[5].split('|')
                bin = db_station.updateStation(splitData[2], reply[2], splitData[0])
                requestReply = jsonFormat({
                    "station_id": data['station_id'],
                    "job_id": reply[4],
                    "status": "true",
                    "message": "Station has successfully updated bin."}, "")
                socketio.emit('update', requestReply, namespace='/station') 
                # emit('update', requestReply)
                msgToSend = "ST,"+str(data['station_id'])+",S;"
                server.sendMsg("ST"+str(data['station_id']), msgToSend)
        else:
            requestReply = jsonFormat({
                "station_id": data['station_id'],
                "job_id": reply[4],
                "status": "false",
                "message": "Unable to update bin."}, reply)
            # emit('update', requestReply)
            socketio.emit('update', requestReply, namespace='/station') 
    except:
        print(redBright("Socket Update Error"))


@socketio.on("move", namespace='/station')
def StationMoveBin(data):
    try:
        result = db_bin.findPositionBin(int(data['station_id']), int(data['from_pos']))
        print("result endpoint direction is" ,result)
        direction = db_station.getStationByID(int(data['station_id']))
        print("endpoint direction is",direction)
        msgToSend = "ST," + str(data['station_id']) + ",M," + str(data['job_id']) + "," + str(data['from_pos']) + "|" + str(data['to_pos']) + "|" + direction.rotation + "|" + result + ";"
        print("move le",msgToSend)
        reply = checkRequest(int(data['station_id']), msgToSend)
        print("move le reply me",reply,"server.receivedMsgList",server.receivedMsgList)
        if type(reply) is list:
            if(reply[0] == "ACK"):
                print("Station has acknowledged move request")
                # reply = None
                # while reply is None:
                #     if len(server.receivedMsgList) != 0:
                #         reply = server.processReply("ST"+str(data['station_id']))
                #         reply = reply.replace(";", "")
                #         splitedReply = reply.split(',')
                #         print("inside???")
                #         if splitedReply[2] == "J":  # If station feedbacks Job Done
                    
                #             msgToSend = "ACK,"+reply+";"
                #             server.sendMsg("ST"+str(data['station_id']), msgToSend)
                #             requestReply = jsonFormat({
                #                 "station_id": int(data['station_id']),
                #                 "job_id": int(splitedReply[3]),
                #                 "status": "COMPLETED",
                #                 "bin_id": result}, "")
                #             # emit('move', requestReply)
                #             socketio.emit('move', requestReply, namespace='/station') 

                #             # Ask for status from station to update frontend
                #             time.sleep(0.1)
                #             msgToSend = "ST,"+str(data['station_id'])+",S;"
                #             server.sendMsg("ST"+str(data['station_id']), msgToSend)
        else:
            requestReply = jsonFormat({
                "station_id": int(data['station_id']),
                "job_id": data['job_id'],
                "status": "ERROR",
                "bin_id": result}, reply)
            socketio.emit('move', requestReply, namespace='/station') 
            # emit('move', requestReply)
    except Exception as e:
        print(e)