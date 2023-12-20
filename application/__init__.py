from os import path
from flask import Flask, url_for
from flask_login import LoginManager

# from flask_sqlalchemy import SQLAlchemy
from .Auth import auth
from .Views import views

# db = SQLAlchemy()
DATABASE_NAME = "main.db"


def create_app():
    app = Flask(__name__)
    app.config["SECRET_KEY"] = "hfhusgyyjIKjT5d4y8"
    app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{DATABASE_NAME}"

    from .Models.models import User, db

    db.init_app(app)

    if not path.exists(f"../instance/{DATABASE_NAME}"):
        app.app_context().push()
        db.create_all()

    login_manager = LoginManager()
    login_manager.login_view = "auth.login"
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    app.register_blueprint(auth)
    app.register_blueprint(views)
    return app
