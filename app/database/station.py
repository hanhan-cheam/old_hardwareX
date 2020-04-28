# from flask import Blueprint, request, make_response, jsonify
from datetime import datetime as dt
# from .. import db
from app import db
from ..models.station import Station
from simple_chalk import redBright
from ..database.bin import InsertUpdateBin,DeleteBin,findBinByStationId
from app import app

# station_blueprint = Blueprint('station', __name__)


def getStationListByCategory(category):
    try:
        station = list()
        stationList = Station.query.filter_by(category=category).all()
        for s in stationList:
            station.append(s.id)
        # print("station ssss",station)
        return station
    except Exception as e:
        print(redBright(e))
 
def getStationByID(station_id):
    try:
        with app.app_context():
            station = Station.query.get(station_id)
            return station
    except Exception as e:
        print(redBright(e))







# def getStationListByType(type):
#     try:
#         with app.app_context():
#             station = list()
#             stationList = Station.query.filter_by(type=type).all()
#             for row in stationList:
#                 station.append(row.id)
#             print("station here",stationList)
#             return station
#     except Exception as e:
#         print(redBright(e))

def getStationDirection(id):
    try:
        with app.app_context():
            station = Station.query.filter_by(id=id).first()
            return station.rotation
    except Exception as e:
        print(redBright(e))


def updateStation(binName, stationID, position):
    print("update statuin : ",binName,stationID,position)
    try:
        with app.app_context():
            if int(position) == 0:
                InsertUpdateBin(binName, position, stationID)
            elif int(position) == 5:
                DeleteBin(int(stationID), int(position))
            else:
                print("not found position or station id")

            bin = findBinByStationId(int(stationID))
            return bin
    except Exception as e:
        print(redBright(e))