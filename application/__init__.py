from flask import Flask, url_for
from flask_sqlalchemy import SQLAlchemy
from .Auth import auth
from .Views import views


def create_app():
    app = Flask(__name__)
    # app.config.from_prefixed_env()

    # print(app.config)
    app.register_blueprint(auth)
    app.register_blueprint(views)
    return app


# # if __name__ == "__main__":
# # app.run(debug=True)
#
# # from Models.models import test
