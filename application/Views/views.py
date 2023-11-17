from flask import render_template, request, url_for, Blueprint, flash
from flask_login import current_user
from flask_login import login_required
import string

views = Blueprint("views", __name__, template_folder="templates", url_prefix="/vws")

user = {
    "photo": "imgs/image.jpg",
    "name": "Kibuule Noah",
    "freinds": 578,
    "num_messages": 790,
}


@views.route("/dashboard")
@login_required
def dashboard():
    return render_template("dashboard.html", user_name=current_user.name)


@views.route("/profile", methods=["GET", "POST"])
@login_required
def profile():
    # if request.method == "POST":
    #     name = request.form["name"]
    #     if len(name) == 0:
    #         flash("nothing input!!, Name not changed")
    #     elif len(name) < 3:
    #         flash("invalid name, it's too short", category="success")
    #     elif name[0].isdigit():
    #         flash("name can't start with a digit")
    return render_template("profile.html", user=user)


@views.route("/room")
@login_required
def room():
    return render_template("room.html")


# @views.route("/oneonone")
# @login_required
# def one_on_one():
# print(f"\n{current_user}\n")
# return render_template("one_on_one.html", user_name=current_user.name)
