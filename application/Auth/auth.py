from flask import render_template, url_for, Blueprint, request, flash, redirect
from werkzeug.security import generate_password_hash, check_password_hash
from ..Models.models import User, db
from flask_login import login_user, login_required

auth = Blueprint("auth", __name__, template_folder="templates", url_prefix="/auth")


@auth.route("/create", methods=["POST", "GET"])
def create():
    if request.method == "POST":
        form = request.form
        if form:
            print(form)
            user = User.query.filter_by(name=form["name"]).first()
            if user:
                flash("user already exists", category="error")
            else:
                new_user = User(
                    name=form["name"],
                    password=generate_password_hash(form["password1"]),
                )
                db.session.add(new_user)
                db.session.commit()
                login_user(new_user, remember=True)
                return redirect(url_for("views.one_on_one"))
    return render_template("create.html")


@auth.route("/login", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        if request.form:
            form = request.form
            user = User.query.filter_by(name=form["name"]).first()
            if user:
                if check_password_hash(user.password, form["password"]):
                    login_user(user, remember=True)
                    return redirect(url_for("views.one_on_one"))
                else:
                    flash(
                        f"Incorrect password for user name {user.name}",
                        category="error",
                    )
            else:
                flash("User name doest'n exists", category="error")
    return render_template("login.html")
