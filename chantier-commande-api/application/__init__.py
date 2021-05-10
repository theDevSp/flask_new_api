from flask import Flask
from dotenv import load_dotenv
from application.config import configurations as cfg
from flask_restful import Api
from flask_jwt_extended import JWTManager

from application.db import db
from application.ma import ma

def init_app():
    app = Flask(__name__)
    load_dotenv(".env")
    app.config.from_object(cfg['development'])

    db.init_app(app)
    ma.init_app(app)
    api = Api(app)

    @app.before_first_request
    def create_tables():
        db.create_all()

    jwt = JWTManager(app)
    with app.app_context():
        from application.ressources.user import UserLogin,User
        api.add_resource(UserLogin, "/login")
        api.add_resource(User, "/user/<string:username>")

        return app