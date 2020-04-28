from flask import current_app as app
from flask import Blueprint, request, make_response, jsonify
from simple_chalk import greenBright, redBright, blueBright
import threading
from app import server
from app.blueprints.station.common import jsonFormat,checkRequest

@app.route('/')
def home():
    # Landing page.
    return "Hello, World"


# @app.route('/request_weight', methods=["POST"])
# def weight():

#     try:
#         data = request.get_json()

#         msgToSend = "ST,"+str(data['station'])+",W,"+","+data['bin_id']+";"
#         print("Connetcion List here: ", server.connectionList)
#         reply = checkRequest(data['station'], msgToSend)
#         print("Connetcion List V2 here: ", server.connectionList)
#         print("msgToSend",msgToSend)
#         print("Connetcion List V3 here: ", server.connectionList)
#         if type(reply) is list :
#             requestReply = jsonFormat({"weight":reply[5], "bin_id":reply[4], "id":reply[3]}, "")
#         else:
#             requestReply = jsonFormat({"station":data['station']}, reply)
#         return requestReply
#     except:
#         print(redBright("Endpoint Weight Error"))

# @app.route('/station/request_weight', methods=["POST"])
# def weight():
#     try:
#         data = request.get_json()
#         if(data['action'] == "IN"):
#             replyAction = "INCREASE"
#         elif(data['action'] == "OUT"):
#             replyAction = "DECREASE"

#         msgToSend = "ST,"+str(data['station_id'])+",W,"+","+data['bin_id']+ "," +data['action']+";"
#         reply = checkRequest(data['station_id'], msgToSend)
#         print("msgToSend",msgToSend)
#         if type(reply) is list :
#             requestReply = jsonFormat({"weight":reply[6], "bin_id":reply[4],"action":replyAction,"station_id":data['station_id']}, "")
#         else:
#             requestReply = jsonFormat({"station_id":data['station_id']}, reply)
#         return requestReply
#     except:
#         print(redBright("Endpoint Weight Error"))
 

