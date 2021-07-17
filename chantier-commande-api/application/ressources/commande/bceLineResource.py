from flask_restful import Resource
from flask import request

from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    get_jwt_identity,
    jwt_required,
)
from application.models.commande.bceLineModel import BceLineModel
from application.models.userModel import UserModel
from application.om import OdooModel as om

class BceLineResource(Resource):

    models = ['article.commande',]

    @classmethod
    @jwt_required()
    def get(cls):
        bce_line_id = request.args.get('id', default = 0, type = int)
        bce_id = request.args.get('bce_id', default = 0, type = int)
        fields = request.args.get('fd',default="", type= str )
        user_public_id = get_jwt_identity()
        user = UserModel.find_by_public_id(user_public_id)

        if om.check_access_rights(user,'read',*cls.models) == True:
            if bce_line_id:    
                return BceLineModel.get_bce_line_by_id(bce_line_id,user,fields.split(',')) if fields else BceLineModel.get_bce_line_by_id(bce_line_id,user)
            if bce_id:    
                return BceLineModel.get_bce_line_by_bce_id(bce_id,user,fields.split(',')) if fields else BceLineModel.get_bce_line_by_bce_id(bce_id,user)
        else:
            return om.check_access_rights(user,'read',*cls.models)
    
    @classmethod
    @jwt_required()
    def post(cls):
        bce_line_json = request.get_json()
        
        user_public_id = get_jwt_identity()
        user = UserModel.find_by_public_id(user_public_id)

        if om.check_access_rights(user,'create',*cls.models) == True:
            return BceLineModel.create_bce_line(bce_line_json,user)
        else:
            return om.check_access_rights(user,'create',*cls.models)

    @classmethod
    @jwt_required()
    def put(cls,bce_line_id:int):  
        bce_line_json = request.get_json()

        user_public_id = get_jwt_identity()
        user = UserModel.find_by_public_id(user_public_id)
        
        
        if om.check_access_rights(user,'write',*cls.models) == True:
            return BceLineModel.update_bce_line(bce_line_id,bce_line_json,user)
        else:
            return om.check_access_rights(user,'write',*cls.models)

    @classmethod
    @jwt_required()
    def delete(cls,bce_line_id:int):
        user_public_id = get_jwt_identity()
        user = UserModel.find_by_public_id(user_public_id)

        if om.check_access_rights(user,'unlink',*cls.models) == True:
            return {"msg": BceLineModel.delete_bce_line(bce_line_id,user)}
        else:
            return om.check_access_rights(user,'unlink',*cls.models)