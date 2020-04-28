from datetime import datetime as dt
from ..models.fake_bin_weight import FakeBinWeight
from app import db
from app import app

#fake bin weight
def resetFakeBinWeight(bin_id = None):
    with app.app_context():
        if bin_id == None:
            db.session.query(FakeBinWeight).delete()
            db.session.commit()
            return "reset all success"
        else:
            db.session.query(FakeBinWeight).filter(FakeBinWeight.bin_id==bin_id).delete()
            db.session.commit()
            
            return "reset "+ bin_id +" success"

def findfakeBinExists(bin_id):
    with app.app_context():
        result = FakeBinWeight.query.filter(FakeBinWeight.bin_id == bin_id).first()
        if result == None:
            return 1
        else:
            return 0
 
def findfakeBinWeight(bin_id):
    with app.app_context():
        result = FakeBinWeight.query.filter(FakeBinWeight.bin_id == bin_id).first()
        if result == None:
            return 0
        else:
            return int(result['weight'])
 
def CreateUpdatefakeBinWeight(bin_id, weight, check):
    with app.app_context():
        if check == 1:
        #     print("no bin id exists,will create new one")
        
            new_fake_bin_weight = FakeBinWeight(
                bin_id = bin_id,
                weight = int(weight)
            )
            db.session.add(new_fake_bin_weight)
            db.session.commit()

            return "created"
        else:

            db.session.query(FakeBinWeight).filter(FakeBinWeight.bin_id == bin_id).update({FakeBinWeight.weight : weight},synchronize_session = False)
            db.session.commit()

            return "updated"
#fake bin weight