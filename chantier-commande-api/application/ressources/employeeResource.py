from flask_restful import Resource
from flask import request

from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    get_jwt_identity,
    jwt_required,
)
from application.models.employyeModel import EmployeeModel
from application.models.userModel import UserModel
from application.om import OdooModel as om

class EmployeeResource(Resource):

    models = ['hr.employee',]

    @classmethod
    @jwt_required()
    def get(cls):
        emp_id = request.args.get('id', default = 0, type = int)
        ch_id = request.args.get('ch_id', default = 0, type = int)
        user_public_id = get_jwt_identity()
        user = UserModel.find_by_public_id(user_public_id)
 
        if om.check_access_rights(user,'read',*cls.models) == True:
            if emp_id:    
                return EmployeeModel.get_employee_by_id(emp_id,user)
            if ch_id:    
                return EmployeeModel.get_employee_by_ch_id(ch_id,user)
        else:
            return om.check_access_rights(user,'read',*cls.models)