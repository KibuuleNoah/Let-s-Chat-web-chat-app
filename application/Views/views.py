from flask import json, render_template, request, url_for, Blueprint, flash, jsonify
from flask_login import current_user, login_required

from ..functions import *
from ..Models.models import Message, Room, User, db


views = Blueprint("views", __name__, template_folder="templates", url_prefix="/vws")


# dashboard route
@views.route("/", methods=["GET", "POST"])
@login_required
def dashboard():
    user_img = get_user_img(current_user.id)
    # lists all rooms
    rooms = Room.query.all()
    your_rooms = [rm for rm in rooms if rm.creater_id == current_user.id]
    other_rooms = [rm for rm in rooms if not (rm.creater_id == current_user.id)]
    return render_template(
        "index.html",
        user_name=current_user.name,
        your_rooms=your_rooms,
        other_rooms=other_rooms,
        img_data=user_img,
    )


# profile route. for displaying and updating user information
@views.route("/profile", methods=["GET", "POST"])
@login_required
def profile():
    """
    profile route. for displaying and updating user information
    """
    user_img_data = get_user_img(current_user.id)
    if request.method == "POST":
        data = request.data
        data = json.loads(data) if data else {}
        image_data = data.get("imageData", "")  # data.get("imageData")

        new_name = request.form.get("name")
        old_password = request.form.get("password")
        new_password = request.form.get("password2")
        if new_name:
            update_user_name(new_name)
        elif old_password and new_password:
            update_user_password(old_password, new_password)

        # fetches newly uploaded image
        # prof_img = request.files.get("img-input")
        if image_data:
            # print(image_data)
            image_data = convert_to_bytes(image_data.split(",", 1)[-1])
            # updates user photo
            User.query.filter_by(id=current_user.id).update({User.photo: image_data})
            db.session.commit()
            return jsonify({"message": "Image uploaded successfully"})

    return render_template("profile.html", user=current_user, img_data=user_img_data)


# settings route for rendering settings page
@views.route("/settings/<room_id>", methods=["POST", "GET"])
@login_required
def settings(room_id):
    """
    settings route for rendering settings page
    """
    if request.method == "POST":
        new_room_name = request.form.get("room-name", "")
        new_room_moto = request.form.get("room-moto", "")

        # print("UPDATE", new_room_name)
        # print("UPDATE", new_room_moto)
        data = request.data
        data = json.loads(data) if data else {}
        new_room_image_data = data.get("imageData", "")
        new_room_image_bytes = convert_to_bytes(new_room_image_data.split(",", 1)[-1])
        update_room_info(
            int(room_id), new_room_name, new_room_moto, new_room_image_bytes
        )
    return render_template("settings.html")


@views.route("/delete-room", methods=["POST"])
def delete_room():
    room = json.loads(
        request.data
    )  # this function expects a JSON from the INDEX.js file
    roomId = room["roomId"]
    print("ROOMTOREL", roomId)
    room = Room.query.get(roomId)
    # print(room)
    if room and (room.creater_id == current_user.id):
        db.session.execute(db.delete(Message).filter_by(room_id=roomId))

        db.session.delete(room)
        db.session.commit()
    return jsonify({})


@views.route("/GMSI", methods=["POST"])
def get_msg_sender_info():
    """
    Gets massage sender infomation basing on the received user id
    """
    data = json.loads(request.data)
    # print(data)
    sender_id = data["sender_id"]
    user = User.query.get(sender_id)
    user_name = user.name
    # converts an image to a web base64
    user_photo = convert_to_base64(user.photo)
    return jsonify({"name": user_name, "photo": user_photo})


@views.app_template_filter("to_base64")
def to_base64(s):
    """
    A simple jinja filter to convert a byte image to a base64 data
    """
    return convert_to_base64(s)


@views.app_template_filter("truct")
def truct(text):
    """
    A simple jinja filter used for shortening long text
    """
    return text[:10] + "..." if len(text) > 10 else text
