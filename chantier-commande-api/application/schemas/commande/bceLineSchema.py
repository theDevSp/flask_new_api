from application.schemas.documentsLineSchema import DocumentsLineSchema
from marshmallow import fields,post_load
from application.models.commande.bceLineModel import BceLineModel


class BceSchema(DocumentsLineSchema):

    __model__ = BceLineModel

    name = fields.Str()
    price_bord_id = fields.Integer()
    bce_id = fields.Integer()
    