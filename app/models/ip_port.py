from dataclasses import dataclass
# from .. import db
from app import db

@dataclass
class IpPort(db.Model):
    id: int
    ip : str
    port : str
    name : str
    station_id : int
    created_at : str
    updated_at : str

    __tablename__ = 'ip_ports'
    id = db.Column(
        db.Integer,
        primary_key=True
    )

    ip = db.Column(
        db.String(64),
        index=False,
        unique=False,
        nullable=False
    )

    station_id = db.Column(
        db.Integer
    )

    port = db.Column(
        db.String(64),
        index=False,
        unique=False,
        nullable=False
    )

    name = db.Column(
        db.String(80),
        index=False,
        unique=False,
        nullable=False
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
        return '<IpPort {}>'.format(self.ip)