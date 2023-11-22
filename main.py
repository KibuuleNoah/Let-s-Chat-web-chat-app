from flask import request
from flask_socketio import SocketIO, emit, join_room
from application import create_app
from flask_login import current_user
from application.Views.views import get_user_img
from application.Models.models import User, Message, Room, db
from time import strftime
import time

# from application.Auth.auth import models
joined_users = set()

app = create_app()
socketio = SocketIO(app)


@socketio.on("connect")
def connection():
    print("connected")


@socketio.on("join")
def handle_join_one(roomObj):
    room = Room.query.filter_by(room_name=roomObj["room"]).first()
    room_msgs = room.messages
    print([[msgobj.sender_id, msgobj.message, msgobj.id] for msgobj in room_msgs])
    sid = request.sid
    join_room(roomObj["room"])
    print(sid, "joined -> ", roomObj["room"])
    emit("send_ids", {"user_id": current_user.id, "room": roomObj["room"]})
    emit(
        "get_room_messages",
        [
            [
                # get sender image by using the sender id
                get_user_img(msgobj.sender_id),
                msgobj.sender_id,
                msgobj.message,
            ]
            for msgobj in room_msgs
        ],
    )


def save_message(msg, sender_id, room):
    print("saving to the database")
    print(msg, sender_id, room)


@socketio.on("create_room")
def create_room(roomObj):
    room, moto = roomObj.values()
    # data = request.get_json()
    # image_data = data.get("imageData")
    rooms = [rm.room_name for rm in Room.query.all() if rm]
    print(f"rooms: \n{rooms}\n")
    if room in rooms:
        emit("confirm_room_exists", True)
    rooms.append(room)
    # if not image_data:
    with open("room.bin", "rb") as image:
        image_data = image.read()
    # save created room to the database
    new_room = Room(
        room_name=room,
        room_moto=moto,
        creater_id=current_user.id,
        image=image_data.encode(),
    )
    db.session.add(new_room)
    db.session.commit()
    emit("confirm_room_exists", False)


@socketio.on("message")
def handle_messsage(msgObj):
    msg, room, sender_id = msgObj.values()
    print(msg, " for ", room, "from", sender_id)
    curr_usr_id = current_user.id
    curr_time = strftime("%I:%M:%S %p")
    room_data = Room.query.filter_by(room_name=room).first()
    # save message to the database
    new_msg = Message(message=msg, sender_id=sender_id, room_id=room_data.id)
    db.session.add(new_msg)
    db.session.commit()
    msgObj = {"message": msg, "id": curr_usr_id, "time": curr_time}
    emit("message", msgObj, broadcast=True, room=room)


@socketio.on("test")
def test(n):
    print(n)


if __name__ == "__main__":
    socketio.run(app, debug=True)
#
# # Example of updating data based on column1
# YourModel.query.filter(YourModel.column1 == 'old_value').update({YourModel.column1: 'new_value'})
# db.session.commit()
#
# class YourModel(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     column1 = db.Column(db.String(50))
#     column2 = db.Column(db.String(50))
#
# # Example of selecting data based on column1
# result = YourModel.query.filter(YourModel.column1 == 'desired_value').all()
#
