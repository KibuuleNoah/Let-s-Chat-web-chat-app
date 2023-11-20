from flask import render_template, request, url_for, Blueprint, flash
from flask_login import current_user
from flask_login import login_required
from ..Models.models import Room
import string

views = Blueprint("views", __name__, template_folder="templates", url_prefix="/vws")

user = {
    "photo": "imgs/image.jpg",
    "name": "Kibuule Noah",
    "freinds": 578,
    "num_messages": 790,
}


@views.route("/dashboard", methods=["GET", "POST"])
@login_required
def dashboard():
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
    )


@views.route("/profile", methods=["GET", "POST"])
@login_required
def profile():
    return render_template("profile.html", user=user)


@views.route("/room")
@login_required
def room():
    return render_template("room.html")
