from flask import request, jsonify
from flask.json import loads
from flask_socketio import SocketIO, emit, join_room
from socketio.zmq_manager import re
from application import create_app
from flask_login import current_user
from application.Views.views import get_user_img
from application.Models.models import User, Message, Room, db
from application.functions import convert_to_bytes, convert_to_base64
from time import strftime
import time

joined_users = set()

app = create_app()
socketio = SocketIO(app)


def save_message(msg, sender_id, room_id):
    new_msg = Message(message=msg, sender_id=sender_id, room_id=room_id)
    db.session.add(new_msg)
    db.session.commit()


def create_room_now(name, moto, image_data):
    new_room = Room(
        room_name=name,
        room_moto=moto,
        creater_id=current_user.id,
        image=image_data,
    )

    db.session.add(new_room)
    db.session.commit()


def get_time_from_datetime(string):
    print(re.search(r"\d{2}:\d{2}", str(string)).group())
    return re.search(r"\d{2}:\d{2}", str(string)).group()


def convert_24_to_12(time_str):
    hr = int(time_str[:2])
    conv_hr = hr - 12 if hr > 12 else (12 if hr == 0 else hr)
    am_pm = "am" if hr < 12 else "pm"
    return f"{conv_hr}:{time_str[3:]}{am_pm}"


def get_MSI(sender_id):
    print(sender_id)
    if not (sender_id == current_user.id):
        user = User.query.get(sender_id)
        print(user)
        return [user.name, convert_to_base64(user.photo)]
    return ["", ""]


@socketio.on("connect")
def connection():
    pass
    # print("connected")


@socketio.on("join")
def handle_join_one(roomObj):
    """
    performs some actions when the client joins the room
    """
    room = Room.query.filter_by(room_name=roomObj["room"]).first()

    if room:
        room_msgs = room.messages
        join_room(roomObj["room"])

        # print(sid, "joined -> ", roomObj["room"])
        emit("send_ids", {"user_id": current_user.id, "room": roomObj["room"]})
        emit(
            "get_room_messages",
            sorted(
                [
                    [
                        # get sender image by using the sender id
                        msgobj.id,
                        msgobj.sender_id,
                        *get_MSI(msgobj.sender_id),
                        msgobj.message,
                        convert_24_to_12(get_time_from_datetime(msgobj.time)),
                    ]
                    for msgobj in room_msgs
                ]
            ),
        )


# endpoint for creating a room
@socketio.on("create_room")
def create_room(roomObj):
    room_name, moto = roomObj.values()
    print(room_name, moto, end="\n")
    rooms = [rm.room_name for rm in Room.query.all() if rm]
    print(f"rooms: \n{rooms}\n")
    if room_name in rooms:
        emit("confirm_room_exists", True)
    emit("confirm_room_exists", False)
    rooms.append(room_name)
    with open("room.bin", "rb") as image:
        image_data = image.read()
    # save created room to the database
    create_room_now(room_name, moto, image_data)


@socketio.on("message")
def handle_messsage(msgObj):
    msg, room, sender_id = msgObj.values()
    print(msg, " for ", room, "from", sender_id)
    curr_usr_id = current_user.id
    curr_time = strftime("%I:%M:%S %p")
    room_data = Room.query.filter_by(room_name=room).first()
    # save message to the database
    save_message(msg, sender_id, room_data.id)

    msgObj = {"message": msg, "id": curr_usr_id, "time": curr_time}
    emit("message", msgObj, broadcast=True, to=room)


@socketio.on("bounce-save")
def bounce_save(data):
    print("receiving .......")
    image_data = convert_to_bytes(data["imageData"].split(",", 1)[-1].encode())
    Room.query.filter_by(room_name=data["args"][0]).update({Room.image: image_data})
    db.session.commit()
    print("emittinig.......")
    emit("room_img", {"imageData": data["imageData"]})
    print("emitted")


@app.route("/GRI", methods=["POST"])
def get_room_image():
    data = loads(request.data)
    room_name = data["roomName"]
    room = Room.query.filter_by(room_name=room_name).first()
    if room:
        return jsonify({"imageData": convert_to_base64(room.image)})
    return jsonify({})


if __name__ == "__main__":
    socketio.run(app, debug=True)
