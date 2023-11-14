from flask import render_template, request, url_for, Blueprint, flash
import string

views = Blueprint("views", __name__, template_folder="templates", url_prefix="/vws")

user = {
    "photo": "imgs/image.jpg",
    "name": "Kibuule Noah",
    "freinds": 578,
    "num_messages": 790,
}

# @views.route("/dashbord")
# def dashbord():
# return render_template("")


@views.route("/profile", methods=["GET", "POST"])
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
def room():
    return render_template("room.html")


@views.route("/oneonone")
def one_on_one():
    return render_template("one_on_one.html")
