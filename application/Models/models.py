from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime

db = SQLAlchemy()


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    photo = db.Column(db.LargeBinary, nullable=False)
    joined = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    messages = db.relationship("Message")
    rooms = db.relationship("Room")


class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    message = db.Column(db.Text, nullable=False)
    sender_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    room_id = db.Column(db.Integer, db.ForeignKey("room.id"), nullable=False)
    time = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)


class Room(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    room_name = db.Column(db.String(15), nullable=False, unique=True)
    room_moto = db.Column(db.String, nullable=False)
    creater_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    image = db.Column(db.LargeBinary, nullable=False)
    create_date_time = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    num_clients = db.Column(db.Integer, nullable=False, default=0)
    messages = db.relationship("Message")
    users = db.relationship("User")
