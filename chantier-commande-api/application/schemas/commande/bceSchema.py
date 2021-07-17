from application.schemas.documentsSchema import DocumentsSchema
from marshmallow import fields,post_load
from application.models.commande.bceModel import BceModel


class BceSchema(DocumentsSchema):

    __model__ = BceModel

    type = fields.Str()
    service = fields.Str()

