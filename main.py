from flask import request
from flask_socketio import SocketIO, emit, join_room
from application import create_app
from flask_login import current_user
from time import strftime
import time

# from application.Auth.auth import models
room_ = ""


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
    rooms = ["room"]
    if room in rooms:
        emit("confirm_room_exists", True)
    print(room, "CREATED \n")
    emit("confirm_room_exists", False)


@socketio.on("message-one")
def handle_messsage_one(msgObj):
    msg, room = msgObj.values()
    print(msg, " for ", room)
    curr_usr_id = current_user.id
    curr_time = strftime("%I:%M:%S %p")
    d = {"message": msg, "id": curr_usr_id, "time": curr_time}
    emit("message-one", d, broadcast=True, room=room)


if __name__ == "__main__":
    socketio.run(app, debug=True)
