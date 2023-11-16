from flask import request
from flask_socketio import SocketIO, emit, join_room
from application import create_app
from flask_login import current_user
from time import strftime
import time

# from application.Auth.auth import models
room = ""


app = create_app()
socketio = SocketIO(app)


@socketio.on("connect")
def connection():
    print("connected")


@socketio.on("user_join_one")
def handle_join_one(roomObj):
    # id = current_user.id
    sid = request.sid
    # print(id)
    global room
    room = roomObj
    join_room(room, sid)
    print(sid, "joined -> ", room)
    # time.sleep(5)
    # print("\nEMITTing\n")
    # emit("send_ids", {"user_id": id, "user_sid": sid, "room": room})
    # print(f"\n EMITTED \n")
    # emit("one_on_one", {"users_id": id, "user_sid": sid, "room": room["room"]})


@socketio.on("reach")
def reach(k):
    print("***********", room)
    emit("send_ids", {"user_id": current_user.id, "room": room})


@socketio.on("message-one")
def handle_messsage_one(msgObj):
    # print(msgObj["message"])
    print(msgObj)
    current_time = strftime("%I:%M:%S %p")
    d = {"message": msgObj["message"], "id": current_user.id, "time": current_time}
    emit("message-one", d, broadcast=True, room="room1")


if __name__ == "__main__":
    socketio.run(app)
