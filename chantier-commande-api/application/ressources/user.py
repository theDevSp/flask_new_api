from flask_restful import Resource
from flask import request
from werkzeug.security import safe_str_cmp
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    get_jwt_identity,
    jwt_required,
)
from application.models.userModel import UserModel
from application.schemas.user import UserSchema
from application.blacklist import BLACKLIST
import uuid
from cryptography.fernet import Fernet
from application.om import OdooModel as om
import base64


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
    def get(cls, username: str):
        user = UserModel.find_by_username(username)
        if not user:
            return {"message": gettext("user_not_found")}, 404
        
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
        
        uid = oCommon.authenticate(oDB, username, password, {})
        
        if uid:

            encrypted_pass = UserModel.encryptMsg(password)
            new_user = {'uid':uid,'username':username,'password':encrypted_pass,'public_id':str(uuid.uuid4())}
            user_if_exist = UserModel.find_by_username(username)
            user = user_schema.load(new_user)
            identity = None
            if user_if_exist:
                identity = user_if_exist.public_id = str(uuid.uuid4())
                user_if_exist.save_to_db()
            else:
                identity = new_user.get('public_id',0)
                user.save_to_db()

            print(om.check_access_rights(user,'public.market','write'))
            access_token = create_access_token(identity=identity, fresh=True)
            refresh_token = create_refresh_token(new_user.get('public_id',0))

            return {"access_token": access_token, "refresh_token": refresh_token}, 200

        return {"message": "user_invalid_credentials"}, 401


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
