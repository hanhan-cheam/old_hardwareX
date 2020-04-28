from dataclasses import dataclass
# from .. import db
from app import db

@dataclass
class User(db.Model):
    id: int
    username: str
    email: str
    fullname: str
    created: str

    __tablename__ = 'users'
    id = db.Column(
        db.Integer, 
        primary_key=True
    )
    username = db.Column(
        db.String(64),
        index=False,
        unique=True,
        nullable=False
    )
    email = db.Column(
        db.String(80),
        index=True,
        unique=True,
        nullable=False
    ) 
    fullname = db.Column(
        db.String(128),
        index=False,
        unique=False,
        nullable=True
    )
    created = db.Column(
        db.DateTime,
        index=False,
        unique=False,
        nullable=False
    )
    
    def __repr__(self):
        return '<User {}>'.format(self.username)