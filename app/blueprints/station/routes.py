from flask import Blueprint, request, make_response, jsonify
from datetime import datetime as dt
# from .. import db
from ..station import station_blueprint
from simple_chalk import redBright
from .common import jsonFormat,checkRequest
# from app.database import station as db_station
# from app.database import bin as db_bin
from ...database import station as db_station
from ...database import bin as db_bin
from ...database import fakebinweight as db_fakebinweight
from app import server
import threading
@station_blueprint.route('/')
def home():
    # Landing page.
    x = threading.Thread(target=server.startServer)
    x.start()
    json = jsonFormat({"bins": "test2", "direction": "test"}, "")
    return json


    

@station_blueprint.route("/station_list", methods=["POST"])
def GetStationListByType():
    try:
        data = request.get_json()
        station = db_station.getStationListByCategory(data['type'])
        # print("station is",station)
        json = jsonFormat({"stations": station}, "")
        return json
    except:
        print(redBright("Endpoint getStationListByCategory Error"))


@station_blueprint.route('/get_station', methods=["POST"])
def GetCurrentStation():
    try:
        data = request.get_json()
        result = db_station.getStationByID(data['station_id'])
        print("direction",result)
        bin = db_bin.findBinByStationId(data['station_id'])
        json = jsonFormat({"bins": bin, "direction": result.rotation}, "")
        return json
    except:
        print(redBright("Endpoint GetCurrentStation Error"))



@station_blueprint.route('/request_weight_demo', methods=["POST"])
def weight_demo():
    try:
        data = request.get_json()
        if(data['action'] == "IN"):
            replyAction = "CHARGE IN"
        elif(data['action'] == "OUT"):
            replyAction = "CHARGE OUT"

        msgToSend = "ST,"+str(data['station_id'])+","+"W"+","+data['bin_id']+ "," +data['action']+";"
        reply = checkRequest(data['station_id'], msgToSend)
        print("msgToSend",msgToSend)
        if type(reply) is list :
            requestReply = jsonFormat({"weight":reply[5], "bin_id":reply[3],"action":replyAction,"station_id":data['station_id']}, "")
        else:
            requestReply = jsonFormat({"station_id":data['station_id']}, reply)
        return requestReply
    except:
        print(redBright("Endpoint Weight Error"))



@station_blueprint.route('/request_weight', methods=["POST"])
def weight():
    try:
        data = request.get_json()
        msgToSend = "ST,"+str(data['station_id'])+",W,"+data['bin_id'] + ";"
        reply = checkRequest(data['station_id'], msgToSend)
 
        if type(reply) is list :
            requestReply = jsonFormat({
                "station_id": data['station_id'],
                "bin_id": reply[3],
                "weight": reply[4]}, "")
        else:
            requestReply = jsonFormat({"station_id": data['station_id']}, reply)
        return requestReply
    except Exception as e:
        print(redBright(e))





@station_blueprint.route('/reset', methods=["GET"])
def reset_all():
    return db_fakebinweight.resetFakeBinWeight()

 

@station_blueprint.route('/reset/<bin_id>', methods=["GET"])
def reset_spawn(bin_id):
    return db_fakebinweight.resetFakeBinWeight(bin_id)

