from application.models.documentsLineModel import DocumentsLineModel
from marshmallow import Schema,fields,post_load

class DocumentsLineSchema(Schema):

    __model__ = DocumentsLineModel

    id = fields.Integer()
    product = fields.Str()
    qty = fields.Str()
    note = fields.Str()
    engin = fields.Integer()
    created_by = fields.Str()
    create_date = fields.DateTime()
    write_date = fields.DateTime()

    @post_load
    def make_user(self,data, **kwargs):
        return self.__model__(**data)