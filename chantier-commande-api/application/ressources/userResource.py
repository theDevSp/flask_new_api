import datetime
from flask_restful import Resource
from flask import request
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    get_jwt_identity,
    jwt_required,
)
from application.models.userModel import UserModel
from application.schemas.userSchema import UserSchema
from application.models.chantierModel import ChantierModel
from application.blacklist import BLACKLIST
import uuid
from cryptography.fernet import Fernet
from application.om import OdooModel as om
import base64
from sqlalchemy import create_engine


user_schema = UserSchema()
oModel = om.ODOO_MODEL
oCommon = om.ODOO_COMMON
oDB = om.ODOO_DB


class UserRegister(Resource):

    @classmethod
    def post(cls):
        user_json = request.get_json()
        user = user_schema.load(user_json)

        if UserModel.find_by_username(user.username):
            return {"message": gettext("user_username_exists")}, 400

        user.save_to_db()

        return {"message": gettext("user_registered")}, 201


class User(Resource):
    """
    This resource can be useful when testing our Flask app. We may not want to expose it to public users, but for the
    sake of demonstration in this course, it can be useful when we are manipulating data regarding the users.
    """

    @classmethod
    @jwt_required()
    def get(cls):
        public_id = get_jwt_identity()
        user = UserModel.find_by_public_id(public_id)
        if not user:
            return {"msg": "user not found"}, 404
        
        return user_schema.dump(user), 200

    @classmethod
    @jwt_required()
    def put(cls):
        public_id = get_jwt_identity()
        user = UserModel.find_by_public_id(public_id)
        if not user:
            return {"msg": "user not found"}, 404
        else:
            user.role = UserModel.get_user_infos(public_id=public_id)['role']
            user.save_to_db()
        
        return user_schema.dump(user), 200

    @classmethod
    def delete(cls, user_id: int):
        user = UserModel.find_by_id(user_id)
        if not user:
            return {"message": gettext("user_not_found")}, 404

        user.delete_from_db()
        return {"message": gettext("user_deleted")}, 200


class UserLogin(Resource):
    @classmethod
    def post(cls):
        
        

        user_json = request.get_json()
        username = user_json.get('username',None)
        password = user_json.get('password',None)
        
        res = UserModel.login(username,password,user_schema)
        
        if res:

            access_token = create_access_token(identity=res, fresh=True, expires_delta=datetime.timedelta(days=365))
            refresh_token = create_refresh_token(res)
            
            user_data = UserModel.get_user_infos(username=username)
            user = UserModel.find_by_username(username=username)
            chantier_data = ChantierModel.get_chantier_by_user_id(user)
            if user_data:
                return {"access_token": access_token, "refresh_token": refresh_token,"user":user_data,"chantier":chantier_data}, 200

        return {"msg": "Login ou mot de passe incorrect Veuillez réessayer"}, 401


class UserLogout(Resource):
    @classmethod
    @jwt_required
    def post(cls):
        jti = get_raw_jwt()["jti"]  # jti is "JWT ID", a unique identifier for a JWT.
        user_id = get_jwt_identity()
        BLACKLIST.add(jti)
        return {"message": gettext("user_logged_out").format(user_id)}, 200


class TokenRefresh(Resource):
    @classmethod
    #@jwt_refresh_token_required
    def post(cls):
        current_user = get_jwt_identity()
        new_token = create_access_token(identity=current_user, fresh=False)
        return {"access_token": new_token}, 200
