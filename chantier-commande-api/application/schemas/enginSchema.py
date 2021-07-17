from marshmallow import Schema,fields,post_load
from application.models.enginModel import EnginModel

class EnginSchema(Schema):

    id = fields.Integer()
    name = fields.Str()
    plate = fields.Str()
    code = fields.Str()
    desc = fields.Str()
    brand = fields.Str()

    @post_load
    def make_engin(self,data, **kwargs):
        return EnginModel(**data)