from . import db
from datetime import datetime

class User(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    full_name = db.Column(db.String(100), nullable=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=True)
    password = db.Column(db.String(100), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)

    reservations = db.relationship('Reservation', backref='user', lazy=True)

class Parkinglot(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    location_name=db.Column(db.String(100), nullable=False)
    address=db.Column(db.String(200), nullable=False)
    pin_code = db.Column(db.String(6), nullable=False)
    price_per_hour = db.Column(db.Float, nullable=False)
    max_spots = db.Column(db.Integer, nullable=False)

    spots = db.relationship('Parkingspot', backref='lot', lazy=True)

class Parkingspot(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    lot_id=db.Column(db.Integer,db.ForeignKey('parkinglot.id'),nullable=False)
    status = db.Column(db.String(1), default='A') 

    reservations = db.relationship('Reservation', backref='spot', lazy=True)


class Reservation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    spot_id = db.Column(db.Integer, db.ForeignKey('parkingspot.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    start_time = db.Column(db.DateTime, default=datetime.utcnow,nullable=False)
    end_time = db.Column(db.DateTime)
    status = db.Column(db.String(20), default='active')
    cost = db.Column(db.Float)