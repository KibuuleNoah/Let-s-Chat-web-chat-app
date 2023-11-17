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


@socketio.on("message-one")
def handle_messsage_one(msgObj):
    print(msgObj)
    current_time = strftime("%I:%M:%S %p")
    d = {"message": msgObj["message"], "id": current_user.id, "time": current_time}
    emit("message-one", d, broadcast=True, room=msgObj["room"])


if __name__ == "__main__":
    socketio.run(app, debug=True)
