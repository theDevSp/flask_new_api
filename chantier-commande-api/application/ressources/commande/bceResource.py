from re import split
from flask_restful import Resource
from flask import request

from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    get_jwt_identity,
    jwt_required,
)
from application.models.commande.bceModel import BceModel
from application.models.commande.bceLineModel import BceLineModel
from application.models.userModel import UserModel
from application.om import OdooModel as om

class BceResource(Resource):

    models = ['stock.external.move',]

    @classmethod
    @jwt_required()
    def get(cls):
        bce_id = request.args.get('id', default = 0, type = int)
        ch_id = request.args.get('ch_id', default = 0, type = str)
        fields = request.args.get('fd',default="", type= str )
        line_fields = request.args.get('ln_fd',default="", type= str )
        notif = request.args.get('notif',default=False, type= bool )
        start_id = request.args.get('start_id', default = 0, type = int)

        user_public_id = get_jwt_identity()
        user = UserModel.find_by_public_id(user_public_id)

        if om.check_access_rights(user,'read',*cls.models) == True:
            if bce_id: 
                res = BceModel.get_bce_by_id(bce_id,user,fields.split(',')) if fields else BceModel.get_bce_by_id(bce_id,user)
                res[0]['line'] = BceLineModel.get_bce_line_by_bce_id(bce_id,user,line_fields.split(',')) if line_fields else BceLineModel.get_bce_line_by_bce_id(bce_id,user,)
                res[0]['commande']['line_count'] = BceLineModel.get_count_bce_line_by_bce_id(bce_id,user)
                return res
            if ch_id:
                resFinal = []
                for ch in ch_id.split(','):
                    
                    result = BceModel.get_bce_by_ch_id(int(ch),user,fields.split(','),notif=notif,start=start_id) if fields else BceModel.get_bce_by_ch_id(int(ch),user,notif=notif,start=start_id)    
                    if not notif:
                        for res in result:
                            res['line'] = BceLineModel.get_bce_line_by_bce_id(res['id'],user,BceLineModel.transform_data(line_fields.split(','))) if line_fields else BceLineModel.get_bce_line_by_bce_id(res['id'],user)
                            res['line_count'] = BceLineModel.get_count_bce_line_by_bce_id(res['id'],user)
                    for r in result:
                        resFinal.append(r)
                
                return resFinal
        else:
            return om.check_access_rights(user,'read',*cls.models)
    
    @classmethod
    @jwt_required()
    def post(cls):
        bce_json = request.get_json()
        
        user_public_id = get_jwt_identity()
        user = UserModel.find_by_public_id(user_public_id)

        if om.check_access_rights(user,'create',*cls.models) == True:
            return BceModel.create_bce(bce_json,user)
        else:
            return om.check_access_rights(user,'create',*cls.models)


    @classmethod
    @jwt_required()
    def put(cls,bce_id):  
        bce_json = request.get_json()

        user_public_id = get_jwt_identity()
        user = UserModel.find_by_public_id(user_public_id)

        if om.check_access_rights(user,'write',*cls.models) == True:
            
            if BceModel.verify_action_permission(bce_id,bce_json,user) == True:
                return BceModel.update_bce(bce_id,bce_json,user)
        else:
            return om.check_access_rights(user,'write',*cls.models)
    
    @classmethod
    @jwt_required()
    def delete(cls,bce_id:int):
        user_public_id = get_jwt_identity()
        user = UserModel.find_by_public_id(user_public_id)

        if om.check_access_rights(user,'unlink',*cls.models) == True:
            return {"msg": BceModel.delete_bce(bce_id,user)}
        else:
            return om.check_access_rights(user,'unlink',*cls.models)