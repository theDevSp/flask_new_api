from flask import current_app
from application.om import OdooModel as om

oModel = om.ODOO_MODEL
oCommon = om.ODOO_COMMON
oDB = om.ODOO_DB

class NumPrixModel():

    _model_market = 'public.market'
    _model_market_template = 'public.market.attachement.template'
    _model_market_template_line = 'public.market.attachement.template.line'

    def __init__(self,id,name,number):
        self.id = id
        self.name = name
        self.number = number
        

    @classmethod
    def get_price_numbers_by_ch_id(cls,ch_id,user):
        res = []

        market_id = oModel.execute_kw(oDB, user.uid, user.decryptMsg(user.password),
                        cls._model_market, 'search',
                        [[['chantier_id', '=', ch_id]]])

        template_id = oModel.execute_kw(oDB, user.uid, user.decryptMsg(user.password),
                        cls._model_market_template, 'search',
                        [[['code', '=', market_id]]])

        prices_list = oModel.execute_kw(oDB, user.uid, user.decryptMsg(user.password),
                        cls._model_market_template_line, 'search_read',
                        [[['attachement_id', '=', template_id]]],
                        {'fields': ['name','price_number','quantity','uom']})

        for price in prices_list:
            res.append({
                "id":price.get("id",0),
                "name":price.get("name",0),
                "number":price.get("price_number",0),
                "cps":price.get("quantity",0),
                "uom":price.get("uom",0),
            })
        return res

    @classmethod
    def get_price_numbers_by_id(cls,id,user):
        res = []

        prices_list = oModel.execute_kw(oDB, user.uid, user.decryptMsg(user.password),
                        cls._model_market_template_line, 'search_read',
                        [[['id', '=', id]]],
                        {'fields': ['name','price_number']})

        for price in prices_list:
            res.append({
                "id":price.get("id",0),
                "name":price.get("name",0),
                "number":price.get("price_number",0),
                
            })
        return res