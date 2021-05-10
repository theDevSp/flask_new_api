from marshmallow import Schema,fields,post_load
from application.models.userModel import UserModel


class UserSchema(Schema):
    
    id = fields.Integer()
    uid = fields.Integer()
    username = fields.Str()
    password = fields.Str()
    public_id = fields.Str()
    load_only = ("password",)

    @post_load
    def make_user(self,data, **kwargs):
        return UserModel(**data)
        
