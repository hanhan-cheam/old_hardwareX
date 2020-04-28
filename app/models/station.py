from dataclasses import dataclass
# from .. import db
from app import db

@dataclass
class Station(db.Model):
    id: int
    type : str
    category : str
    created_at : str
    updated_at : str

    __tablename__ = 'stations'
    id = db.Column(
        db.Integer,
        primary_key=True
    )

    type = db.Column(
        db.String(64),
        index=False,
        unique=False,
        nullable=False
    )

    category = db.Column(
        db.String(80),
        index=False,
        unique=False,
        nullable=False
    )

    rotation = db.Column(
        db.String(80),
        index=False,
        unique=False,
        nullable=True
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
        return '<User {}>'.format(self.type)