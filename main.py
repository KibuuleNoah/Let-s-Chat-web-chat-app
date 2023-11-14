from flask_socketio import SocketIO, emit
from application import create_app
from application.Auth.auth import models


app = create_app()
socketio = SocketIO(app)


@socketio.on("connect")
def connection():
    print("connected")


@socketio.on("message-one")
def handle_messsage_one(msg):
    print(msg)
    emit("message-one", "cool")


if __name__ == "__main__":
    socketio.run(app)
