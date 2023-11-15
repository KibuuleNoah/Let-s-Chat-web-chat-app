from flask import request
from flask_socketio import SocketIO, emit, join_room
from application import create_app
from flask_login import current_user
from time import strftime

# from application.Auth.auth import models


app = create_app()
socketio = SocketIO(app)


@socketio.on("connect")
def connection():
    print("connected")


@socketio.on("user_join_one")
def handle_join_one():
    id = current_user.id
    if id >= 10:
        emit("send_ids", id)
    else:
        print(id)
        room = "room1"
        join_room(room, request.sid)
        emit("send_ids", id)


@socketio.on("message-one")
def handle_messsage_one(msg):
    print(msg)
    current_time = strftime("%I:%M:%S %p")
    d = {"message": msg, "id": current_user.id, "time": current_time}
    if current_user.id >= 10:
        emit("message-one", d, broadcast=True)
    # d = {"message": msg, "id": current_user.id, "time": current_time}
    emit("message-one", d, broadcast=True, to="room1")


if __name__ == "__main__":
    socketio.run(app)
