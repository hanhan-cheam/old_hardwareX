from .. import db

class Address(db.Model):
    id: int
    address1: str
    address2: str
    address3: str
    created: str

    __tablename__ = 'addresses'
    id = db.Column(
        db.Integer, 
        primary_key=True
    )
    address1 = db.Column(
        db.String(64),
        index=False,
        unique=True,
        nullable=False
    )
    address2 = db.Column(
        db.String(64),
        index=False,
        unique=True,
        nullable=False
    )
    address3 = db.Column(
        db.String(64),
        index=False,
        unique=True,
        nullable=False
    )
    created = db.Column(
        db.DateTime,
        index=False,
        unique=False,
        nullable=False
    )
    
    def __repr__(self):
        return '<Address {}>'.format(self.address1)