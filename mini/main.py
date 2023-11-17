from flask import Flask, render_template
from flask_socketio import SocketIO, emit, join_room, leave_room

app = Flask(__name__)
socketio = SocketIO(app)


@app.route("/")
def index():
    return render_template("index.html")


@socketio.on("connect")
def handle_connect():
    print("Client connected")


@socketio.on("disconnect")
def handle_disconnect():
    print("Client disconnected")


@socketio.on("join")
def handle_join(data):
    room = data["room"]
    join_room(room)
    emit("message", {"text": "Joined the room: {}".format(room)}, room=room)


@socketio.on("leave")
def handle_leave(data):
    room = data["room"]
    leave_room(room)
    emit("message", {"text": "Left the room: {}".format(room)}, room=room)


@socketio.on("send_message")
def handle_message(data):
    room = data["room"]
    message = data["message"]
    emit("message", {"text": message, "user": data["user"]}, room=room)


if __name__ == "__main__":
    socketio.run(app, debug=True)
