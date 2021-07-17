from marshmallow import Schema,fields,post_load
from application.models.userModel import UserModel


class UserSchema(Schema):
    
    id = fields.Integer(load_only=True)
    uid = fields.Integer(load_only=True)
    username = fields.Str()
    password = fields.Str(load_only=True)
    public_id = fields.Str(load_only=True)
    employee_id = fields.Integer()
    role = fields.Integer()
    

    @post_load
    def make_user(self,data, **kwargs):
        return UserModel(**data)
        
