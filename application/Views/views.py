from flask import json, render_template, request, url_for, Blueprint, flash, jsonify
from flask_login import current_user
from flask_login import login_required
from werkzeug.security import check_password_hash, generate_password_hash

from ..functions.main import convert_to_base64, convert_to_bytes
from ..Models.models import Room, User, db
import string

views = Blueprint("views", __name__, template_folder="templates", url_prefix="/vws")


# gets current user id and returns the user image
def get_user_img(id_):
    user = User.query.get(id_)
    return convert_to_base64(user.photo)


# update user name
def update_user_name(new_name):
    user = User.query.filter_by(name=new_name).first()
    if not user:
        User.query.filter_by(id=current_user.id).update({User.name: new_name})
        db.session.commit()
        flash("Name updated successfully!!")
        return
    flash("User Name already in User, Use another one", category="error")


# updates user password
def update_user_password(old_password, new_password):
    # update user password
    if check_password_hash(current_user.password, old_password):
        pwd_hash = generate_password_hash(new_password)
        User.query.filter_by(id=current_user.id).update({User.password: pwd_hash})
        db.session.commit()
        flash("Password updated successfully!!", category="success")
        return
    flash("You entered an correct old password", category="error")


# updates room info like name and image
def update_room_info(room_id, new_name, new_moto, new_image):
    room = Room.query.get(room_id)
    # Room_ = Room.query.filter_by(id=room_id)
    # .update({Room.room_name: new_name})
    if room.creater_id == current_user.id:
        print("update allowed")
        if new_name:
            Room.query.filter_by(id=room_id).update({Room.room_name: new_name})
            db.session.commit()
        if new_moto:
            Room.query.filter_by(id=room_id).update({Room.room_moto: new_moto})
            db.session.commit()
        if new_image:
            # new_image = convert_to_bytes(new_image.read())
            print(new_image, "DATADATA")
            Room.query.filter_by(id=room_id).update({Room.image: new_image})
            db.session.commit()
            print("updating room image")
    else:
        flash("you can't edit rooms that are not your", category="error")


# dashboard route
@views.route("/dashboard", methods=["GET", "POST"])
@login_required
def dashboard():
    user_img = get_user_img(current_user.id)
    # lists all rooms
    rooms = Room.query.all()
    your_rooms = [rm for rm in rooms if rm.creater_id == current_user.id]
    other_rooms = [rm for rm in rooms if not (rm.creater_id == current_user.id)]
    print(your_rooms)
    print(other_rooms)
    return render_template(
        "dashboard.html",
        user_name=current_user.name,
        your_rooms=your_rooms,
        other_rooms=other_rooms,
        img_data=user_img,
    )


# profile route. for displaying and updating user information
@views.route("/profile", methods=["GET", "POST"])
@login_required
def profile():
    user_img_data = get_user_img(current_user.id)
    # print(user_img, "image data")
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
    if request.method == "POST":
        new_room_name = request.form.get("room-name", "")
        new_room_moto = request.form.get("room-moto", "")

        print("UPDATE", new_room_name)
        print("UPDATE", new_room_moto)
        # new_room_image = request.files.get("room-image")
        data = request.data
        data = json.loads(data) if data else {}
        new_room_image_data = data.get("imageData", "")
        # print("Data_1: ", new_room_image_data)
        new_room_image_bytes = convert_to_bytes(new_room_image_data.split(",", 1)[-1])
        # print("Data_2: ", new_room_image_bytes)
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
    room = Room.query.get(roomId)
    if room and (room.creater_id == current_user.id):
        db.session.delete(room)
        db.session.commit()

    return jsonify({})


@views.route("/GMSI", methods=["POST"])
def get_msg_sender_info():
    data = json.loads(request.data)
    print(data)
    sender_id = data["sender_id"]
    user = User.query.get(sender_id)
    user_name = user.name
    user_photo = convert_to_base64(user.photo)
    return jsonify({"name": user_name, "photo": user_photo})


@views.app_template_filter("to_base64")
def to_base64(s):
    return convert_to_base64(s)


# @views.route("/upload", methods=["POST"])
# def upload():
#     data = request.get_json()
#     image_data = data.get("imageData")
#     # print(image_data)
#     # Process the image_data as needed (e.g., save it to the database)
#
#     return jsonify({"message": "Image uploaded successfully"})
