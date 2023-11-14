from flask import render_template, url_for, Blueprint, request
from ..Models import models

print("GOT ",models.mod)

auth = Blueprint("auth", __name__, template_folder="templates", url_prefix="/auth")


@auth.route("/create", methods=["POST", "GET"])
def create():
    if request.method == "POST":
        if request.form:
            print("\n", request.form, "\n")
    return render_template("create.html")


@auth.route("/login", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        if request.form:
            print("\n", request.form, "\n")
    return render_template("login.html")


# from ..Models.models import test

# from ..Models.models import YourModel
# from ..Models.models import test
