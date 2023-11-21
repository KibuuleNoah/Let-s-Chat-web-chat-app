from flask import render_template, request, url_for, Blueprint, flash
from flask_login import current_user
from flask_login import login_required
from ..Models.models import Room, User, db
import string, base64

views = Blueprint("views", __name__, template_folder="templates", url_prefix="/vws")

user = {
    "photo": "imgs/image.jpg",
    "name": "Kibuule Noah",
    "freinds": 578,
    "num_messages": 790,
}


def get_user_img(id_):
    user = User.query.get(id_)
    with open("test.png", "wb") as f:
        f.write(user.photo)
    return base64.b64encode(user.photo).decode("utf-8")


@views.route("/dashboard", methods=["GET", "POST"])
@login_required
def dashboard():
    user_img = get_user_img(current_user.id)
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


@views.route("/profile", methods=["GET", "POST"])
@login_required
def profile():
    user_img = get_user_img(current_user.id)
    print(user_img, "image data")
    if request.method == "POST":
        prof_img = request.files.get("img-input")
        if prof_img:
            # img_data = base64.b64encode(prof_img.read()).decode("utf-8")
            new_img = prof_img.read()
            print(prof_img)
            usr = User.query.filter_by(id=current_user.id).update({User.photo: new_img})
            # print(usr.photo)
            # print(usr)
            # usr.update()
            print(usr)
            # {User.photo: prof_img.read()}
            # )
            db.session.commit()

    return render_template("profile.html", user=user, img=user_img)


@views.route("/room")
@login_required
def room():
    return render_template("room.html")
