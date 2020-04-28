# from flask import Blueprint, request, make_response, jsonify
from datetime import datetime as dt
# from .. import db
from app import db
from ..models.bin import Bin
from simple_chalk import redBright
from sqlalchemy import and_, update
# bin_blueprint = Blueprint('bin', __name__)
from app import app
import datetime

def findPositionBin(station_id, position):
    print("station id",station_id,"---","position",position)
    try:
        with app.app_context():
            bin = Bin.query.filter(and_(Bin.station_id == int(station_id),Bin.position == int(position))).first()
            print("bin . name us ",bin.name)
            if(bin != None):
                return bin.name
            else:
                print("selected bin either not found or not in given position")
    except Exception as e:
        print(redBright("Database findPositionBin Error"),redBright(e))
    # except:
        # print(redBright("Database findPositionBin Error"))


def InsertUpdateBin(name, position, stationID):
    try:
        with app.app_context():
            result = findPositionBin(int(stationID), int(position))
            print("InsertUpdateBin result is",result)
            if(result != None):
                print("INSIDE IF")
                db.session.query(Bin).filter(Bin.station_id == int(stationID)).filter(Bin.position == int(position)).update({Bin.name : name},synchronize_session = False)
                # db.session.query(Bin).filter_by(Bin.station_id == int(stationID)).filter_by(Bin.position == int(position)).update({Bin.name : name},synchronize_session = False)
                db.session.commit()
            else:
                print("INSIDE ELSE")
                new_bin = Bin(
                    name = name,
                    station_id = int(stationID),
                    position = int(position),
                    status = "AVAILABLE",
                    created_at = datetime.datetime.now(),
                    updated_at = datetime.datetime.now()
                )
                db.session.add(new_bin)
                db.session.commit()
    except:
        print(redBright("Database InsertBin Error"))


def DeleteBin(stationID, position):
    try:
        with app.app_context():
            result = findPositionBin(int(stationID), int(position))

            if(result != None):
                db.session.query(Bin).filter(Bin.station_id==stationID).filter(Bin.position==position).delete()
                db.session.commit()
            else:
                print(redBright("nothing to delete"))
    except:
        print(redBright("Database DeleteBin Error"))


def findBinByStationId(station_id):
    try:
        with app.app_context():
            result = Bin.query.filter(Bin.station_id == station_id).all()
            for x in result:
                print("the result : ",x.name)

            # Differiate the 6+3 and 6
            bin = ['']*6
            
            for i in range(len(bin)):
                for x in result:
                    if(i == x.position):
                        bin[i] = x.name
                        print(str(x.position) + "    -----   " + x.name)
            # print("bin",bin)
            return bin
    except:
        print(redBright("Database findBinByStationID Error"))