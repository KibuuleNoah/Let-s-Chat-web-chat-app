from flask import render_template, request, url_for, Blueprint, flash
from flask_login import current_user
from flask_login import login_required
from werkzeug.security import check_password_hash, generate_password_hash
from ..Models.models import Room, User, db
import string, base64

views = Blueprint("views", __name__, template_folder="templates", url_prefix="/vws")

user = {
    "photo": "imgs/image.jpg",
    "name": "Kibuule Noah",
    "freinds": 578,
    "num_messages": 790,
}


# gets current user id and returns the user image
def get_user_img(id_):
    user = User.query.get(id_)
    with open("test.png", "wb") as f:
        f.write(user.photo)
    return base64.b64encode(user.photo).decode("utf-8")


# update user name
def update_user_name(new_name):
    user = User.query.filter_by(name=new_name).first()
    if not user:
        User.query.filter_by(id=current_user.id).update({User.name: new_name})
        db.session.commit()
        flash("Name updated successfully!!")
        return
    flash("User Name already in User, Use another one", category="error")


def update_user_password(old_password, new_password):
    # update user password
    if check_password_hash(current_user.password, old_password):
        pwd_hash = generate_password_hash(new_password)
        User.query.filter_by(id=current_user.id).update({User.password: pwd_hash})
        db.session.commit()
        flash("Password updated successfully!!", category="success")
        return
    flash("You entered an correct old password", category="error")


# dashboard routr
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
        img=user_img,
    )


# profile route. for displaying and updating user information
@views.route("/profile", methods=["GET", "POST"])
@login_required
def profile():
    user_img = get_user_img(current_user.id)
    # print(user_img, "image data")
    if request.method == "POST":
        new_name = request.form.get("name")
        old_password = request.form.get("password")
        new_password = request.form.get("password2")
        print(new_password)
        print(old_password)
        print(new_name)
        if new_name:
            update_user_name(new_name)
        elif old_password and new_password:
            update_user_password(old_password, new_password)

        # fetches newly uploaded image
        prof_img = request.files.get("img-input")
        if prof_img:
            ...
            # new_img = prof_img.read()
            # print(prof_img)
            # updates user photo
            # User.query.filter_by(id=current_user.id).update({User.photo: new_img})
            # db.session.commit()

    return render_template("profile.html", user=current_user, img=user_img)


@views.route("/settings")
def settings():
    return render_template("settings.html")
