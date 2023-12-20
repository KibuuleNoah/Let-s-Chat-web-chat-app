from flask import flash
from flask_login import current_user

from werkzeug.security import check_password_hash, generate_password_hash
from ..Models.models import Room, User, db
from base64 import b64encode, b64decode


def convert_to_base64(data):
    """
    Coverts bytes data to base64 data
    """
    try:
        return b64encode(data).decode()
    except Exception as e:
        print("ERROR: ", e)


def convert_to_bytes(data):
    """
    Converts base64 data to bytes data
    """
    try:
        return b64decode(data)
    except Exception as e:
        print("ERROR: ", e)


# gets current user id and returns the user image
def get_user_img(id_):
    """
    Get the user base64 image data given user id
    """
    user = User.query.get(id_)
    return convert_to_base64(user.photo)


# update user name
def update_user_name(new_name):
    """
    Updates user name given then new name doesn't exists
    """
    user = User.query.filter_by(name=new_name).first()
    if not user:
        User.query.filter_by(id=current_user.id).update({User.name: new_name})
        db.session.commit()
        flash("Name updated successfully!!")
        return
    flash("User Name already in User, Use another one", category="error")


# updates user password
def update_user_password(old_password, new_password):
    """
    Updates user password
    """
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
    """Updates chat room name, image and moto"""
    room = Room.query.get(room_id)
    # Room_ = Room.query.filter_by(id=room_id)
    # .update({Room.room_name: new_name})
    if room.creater_id == current_user.id:
        # print("update allowed")
        if new_name:
            Room.query.filter_by(id=room_id).update({Room.room_name: new_name})
            db.session.commit()
        if new_moto:
            Room.query.filter_by(id=room_id).update({Room.room_moto: new_moto})
            db.session.commit()
        if new_image:
            # print("DATADATA")
            Room.query.filter_by(id=room_id).update({Room.image: new_image})
            db.session.commit()
            # print("updating room image")
    else:
        flash("you can't edit rooms that are not your", category="error")
