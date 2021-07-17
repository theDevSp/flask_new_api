from flask_restful import Resource
from flask import request

from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    get_jwt_identity,
    jwt_required,
)
from application.models.chantierModel import ChantierModel
from application.models.userModel import UserModel
from application.om import OdooModel as om

class ChantierResource(Resource):

    models = [
            'res.users',
            'fleet.vehicle',
            'fleet.vehicle.chantier',
            'fleet.vehicle.chantier.users',
            ]

    @classmethod
    @jwt_required()
    def get(cls):
        user_public_id = get_jwt_identity()
        user = UserModel.find_by_public_id(user_public_id)
        if om.check_access_rights(user,'read',*cls.models) == True:
            return ChantierModel.get_chantier_by_user_id(user)
        else:
            return om.check_access_rights(user,'read',*cls.models)
