from datetime import datetime
from re import split
import json

from sqlalchemy.sql.schema import FetchedValue
from flask_restful import Resource
from flask import request
from application.models.entries.entriesModel import EntriesModel
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    get_jwt_identity,
    jwt_required,
)

from application.models.userModel import UserModel
from application.om import OdooModel as om

class EntriesResource(Resource):

    models = ['stock.move',]

    @classmethod
    @jwt_required()
    def get(cls):
        
        product = request.args.get('product', default ="", type = str)
        ch_id = request.args.get('ch_id', default ="", type = str)
        year = request.args.get('year',default=str(datetime.now().year), type= str )
        month = request.args.get('month',default=str(datetime.now().month), type= str )
        

        user_public_id = get_jwt_identity()
        user = UserModel.find_by_public_id(user_public_id)

        if om.check_access_rights(user,'read',*cls.models) == True:
            return EntriesModel.get_entries_by_ch_period(int(ch_id),year,month,user) if not product else EntriesModel.get_entries_by_product_period(product,ch_id,year,month,user)
        else:
            return om.check_access_rights(user,'read',*cls.models)