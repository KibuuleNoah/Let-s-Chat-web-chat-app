from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime

db = SQLAlchemy()


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    photo = db.Column(db.LargeBinary, nullable=False)
    joined = db.Column(
        db.DateTime(timezone=True), nullable=False, default=datetime.utcnow
    )
    messages = db.relationship("Message")
    rooms = db.relationship("Room")


class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    message = db.Column(db.Text, nullable=False)
    sender_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    room_id = db.Column(db.Integer, db.ForeignKey("room.id"), nullable=False)
    time = db.Column(
        db.DateTime(timezone=True), nullable=False, default=datetime.utcnow
    )


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


#
#
# # from .extensions import db
# from flaskblog import db, login_manager
# from flask_login import UserMixin
#
#
# @login_manager.user_loader
# def load_user(user_id):
#     return User.query.get(int(user_id))
#
#
# class User(db.Model, UserMixin):
#     id = db.Column(db.Integer, primary_key=True)
#     username = db.Column(db.String(20), unique=True, nullable=False)
#     email = db.Column(db.String(120), unique=True, nullable=False)
#     image_file = db.Column(db.String(20), nullable=False, default="default.jpg")
#     password = db.Column(db.String(60), nullable=False)
#     posts = db.relationship("Post", backref="author", lazy=True)
#
#     def __repr__(self):
#         return f"User('{self.username}', '{self.email}', '{self.image_file}')"
#
#
# class Post(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     title = db.Column(db.String(100), nullable=False)
#     date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
#     content = db.Column(db.Text, nullable=False)
#     user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
#
#     def __repr__


# from flask import request

# @app.route('/upload', methods=['POST'])
# def upload_image():
#     if 'file' not in request.files:
#         return 'No file part'
#
#     file = request.files['file']
#
#     if file.filename == '':
#         return 'No selected file'
#
#     new_image = Image(data=file.read())
#     db.session.add(new_image)
#     db.session.commit()
#
#     return 'Image uploaded successfully'
#
# @app.route('/display/<int:image_id>')
# def display_image(image_id):
#     image = Image.query.get(image_id)
#     if image:
#         return send_file(BytesIO(image.data), mimetype='image/jpeg')
#     else:
#         return 'Image not found'
#
