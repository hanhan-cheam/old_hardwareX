from dataclasses import dataclass
# from .. import db
from app import db

@dataclass
class Bin(db.Model):
    id: int
    status : str
    name : str
    station_id : int
    position : int
    created_at : str
    updated_at : str

    __tablename__ = 'bins'
    id = db.Column(
        db.Integer,
        primary_key=True
    )
    
    name = db.Column(
        db.String(64),
        index=False,
        unique=False,
        nullable=True
    )

    position = db.Column(
        db.Integer
    )

    status = db.Column(
        db.String(64),
        index=False,
        unique=False,
        nullable=False
    )

    station_id = db.Column(
        db.Integer
    )

    created_at = db.Column(
        db.DateTime,
        index=False,
        unique=False,
        nullable=True
    )

    updated_at = db.Column(
        db.DateTime,
        index=False,
        unique=False,
        nullable=True
    )

    def __repr__(self):
        return '<IpPort {}>'.format(self.station_id)