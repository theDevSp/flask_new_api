from marshmallow import Schema,fields,post_load
from application.models.chantierModel import ChantierModel

class ChantierSchema(Schema):

    id = fields.Integer()
    name = fields.Str()
    use = fields.Bool()
    atelier = fields.Bool()

    @post_load
    def make_chantier(self,data, **kwargs):
        return ChantierModel(**data)
