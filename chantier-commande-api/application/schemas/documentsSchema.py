from application.models.documentsModel import DocumentsModel
from marshmallow import Schema,fields,post_load


class DocumentsSchema(Schema):

    __model__ = DocumentsModel

    id = fields.Integer()
    name = fields.Str()
    demandeur = fields.Str()
    note = fields.Str()
    ch_id = fields.Integer()
    created_by = fields.Str()
    create_date = fields.DateTime()
    write_date = fields.DateTime()
    state = fields.Str()

    @post_load
    def make_user(self,data, **kwargs):
        return self.__model__(**data)