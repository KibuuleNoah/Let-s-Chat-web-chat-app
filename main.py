from flask import request
from flask_socketio import SocketIO, emit, join_room
from application import create_app
from flask_login import current_user
from application.Models.models import User, Message, Room, db
from time import strftime
import time

# from application.Auth.auth import models


app = create_app()
socketio = SocketIO(app)


@socketio.on("connect")
def connection():
    print("connected")


@socketio.on("join")
def handle_join_one(roomObj):
    # id = current_user.id
    sid = request.sid
    join_room(roomObj["room"])
    print(sid, "joined -> ", roomObj["room"])
    emit("send_ids", {"user_id": current_user.id, "room": roomObj["room"]})


def save_message(msg, sender_id, room):
    print("saving to the database")
    print(msg, sender_id, room)


@socketio.on("create_room")
def create_room(roomObj):
    room, moto, image = roomObj.values()
    rooms = [rm.name for rm in Room.query.all() if rm]
    print(f"rooms: \n{rooms}\n")
    if room in rooms:
        emit("confirm_room_exists", True)
    # save created room to the database
    new_room = Room(room_name=room, room_moto=moto, creater_id=current_user.id)
    db.session.add(new_room)
    db.session.commit()
    emit("confirm_room_exists", False)


@socketio.on("message")
def handle_messsage_one(msgObj):
    msg, room, sender_id = msgObj.values()
    print(msg, " for ", room, "from", sender_id)
    curr_usr_id = current_user.id
    curr_time = strftime("%I:%M:%S %p")
    room_id = Room.query.all()
    print(room_id)
    # new_msg = Message(message=msg,sender_id=sender_id,room_id)
    msgObj = {"message": msg, "id": curr_usr_id, "time": curr_time}
    emit("message", msgObj, broadcast=True, room=room)


if __name__ == "__main__":
    socketio.run(app, debug=True)
